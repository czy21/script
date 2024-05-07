/*
 * Sonatype Nexus (TM) Open Source Version
 * Copyright (c) 2008-present Sonatype, Inc.
 * All rights reserved. Includes the third-party code listed at http://links.sonatype.com/products/nexus/oss/attributions.
 *
 * This program and the accompanying materials are made available under the terms of the Eclipse Public License Version 1.0,
 * which accompanies this distribution and is available at http://www.eclipse.org/legal/epl-v10.html.
 *
 * Sonatype Nexus (TM) Professional Version is available from Sonatype, Inc. "Sonatype" and "Sonatype Nexus" are trademarks
 * of Sonatype, Inc. Apache Maven is a trademark of the Apache Software Foundation. M2eclipse is a trademark of the
 * Eclipse Foundation. All other trademarks are the property of their respective owners.
*/

/*
 * Utility script that scans blobstores and reads the asset properties files within to summarize which repositories
 * are using the blob store, and how much space each is consuming and how much space could potentially be reclaimed by
 * running a compact blobstore task.
 *
 * The script retrieves the blobstore locations from the Nexus system and also all defined repositories.
 *
 * It is possible to specify a whitelist of repository names *OR* a blacklist (whitelist takes priority)
 * If a whitelist is provided, only those repositories whitelisted will be included.
 * If a blacklist is provided (and no whitelist), any repositories that are blacklisted will be omitted.
 *
 * Any empty repositories are also included.
 *
 * The script tabulates both the total size, and the size that could be reclaimed by performing a compact blob store
 * task.
 *
 * Script was developed to run as an 'Execute Script' task within Nexus Repository Manager.
 *
 * ==== CHANGE LOG ====
 * May 10, 2022
 * - fix Windows path matching
 * May 9, 2022
 * - fix for proper rethrow handling exception caused by failed properties file processing
 * - reduce heap memory by not putting all paths to blob properties files into List object
 * - improve file path matcher patterns to exclude non .properties files and only include files under ./content
 */

 /* ---------------- BEGIN CONFIGURABLE SECTION -------------*

 * Whitelist - a list of repository names that should be the only items included.
 *
 *   For example: REPOSITORY_WHITELIST = ['maven-central', 'npm-hosted']
 */

REPOSITORY_WHITELIST = []

/* Blacklist - a list of repository names that should not be included.
 *   This will only apply if REPOSITORY_WHITELIST is not set
 *
 *   For example: REPOSITORY_BLACKLIST = ['maven-central', 'npm-hosted']
 */

REPOSITORY_BLACKLIST = []

/* ---------------- END CONFIGURABLE SECTION ---------------*/

import groovy.json.JsonOutput
import java.nio.file.FileSystems
import java.nio.file.Path
import java.nio.file.PathMatcher
import java.text.SimpleDateFormat
import java.math.RoundingMode
import org.slf4j.LoggerFactory
import org.sonatype.nexus.common.app.ApplicationDirectories
import org.sonatype.nexus.internal.app.ApplicationDirectoriesImpl

import static groovy.io.FileType.FILES

def log = LoggerFactory.getLogger(this.class)

ApplicationDirectories applicationDirectories = (ApplicationDirectories)container.lookup(ApplicationDirectoriesImpl.class.name)

Map<String,File> blobStoreDirectories = [:]
hasWhitelist = REPOSITORY_WHITELIST.size() > 0
hasBlacklist = !hasWhitelist && REPOSITORY_BLACKLIST.size() > 0

String SEP = FileSystems.getDefault().getSeparator()
if ('\\' == SEP) {
  SEP = "${SEP}${SEP}"  // escape back slashes on windows so path matchers work correctly
log.info("Treating file system as using Windows path separators.")
}

def EXCLUDE_PATTERNS = "glob:{" +
    "**${SEP}metadata.properties," +
    "**${SEP}*metrics.properties," +
    "**${SEP}*.bytes," +
    "**${SEP}tmp*," +
    "**${SEP}*deletions.index," +
    "**${SEP}*.DS_Store}"
log.info("Global Blobstore exclude patterns: {}", EXCLUDE_PATTERNS)
PathMatcher EXCLUDE_MATCHER = FileSystems.getDefault().getPathMatcher(EXCLUDE_PATTERNS)


//Default location of results is the Nexus temporary directory
File resultsFileLocation = applicationDirectories.getTemporaryDirectory()

Map<String, BlobStatistics> blobStatCollection = [:].withDefault { 0 }

class BlobStatistics
{
  int totalRepoNameMissingCount = 0
  long totalBlobStoreBytes = 0
  BigDecimal totalBlobStoreMB = 0
  BigDecimal totalBlobStoreGB = 0
  long totalReclaimableBytes = 0
  BigDecimal totalReclaimableMB = 0
  BigDecimal totalReclaimableGB = 0
  Map<String, RepoStatistics> repositories = [:]
}

class RepoStatistics {
  long totalBytes = 0
  BigDecimal totalMB = 0
  BigDecimal totalGB = 0
  long reclaimableBytes = 0
  BigDecimal reclaimableMB = 0
  BigDecimal reclaimableGB = 0
}

def collectMetrics(final BlobStatistics blobstat, Set<String> unmapped,
                   final Properties properties, final File propertiesFile) {
  def repo = properties.'@Bucket.repo-name'
  if(repo == null && properties.'@BlobStore.direct-path') {
    repo = 'SYSTEM:direct-path'
  }
  if(repo == null) {
    // unexpected - log the unexpected condition
    if(blobstat.totalRepoNameMissingCount <= 50){
      log.warn('Repository name missing from {} : {}', propertiesFile.absolutePath, properties)
      log.info('full details: {}', properties)
    }
    blobstat.totalRepoNameMissingCount++
  } else {
    if (!blobstat.repositories.containsKey(repo)) {
      if (!unmapped.contains(repo)) {
        if (!repo.equals('SYSTEM:direct-path')) {
          log.info('Found unknown repository in {}: {}', propertiesFile.absolutePath, repo)
        }
        blobstat.repositories.put(repo as String, new RepoStatistics())
      }
    }

    if (blobstat.repositories.containsKey(repo)) {
      blobstat.repositories."$repo".totalBytes += (properties.size as long)
      if (!repo.equals('SYSTEM:direct-path')) {
        blobstat.totalBlobStoreBytes += (properties.size as long)
      }

      if (properties.'deleted') {
        blobstat.repositories."$repo".reclaimableBytes += (properties.size as long)
        if (!repo.equals('SYSTEM:direct-path')) {
          blobstat.totalReclaimableBytes += (properties.size as long)
        }
      }
    }
  }
}

def passesWhiteBlackList(final String name) {
  if (hasWhitelist) {
    return REPOSITORY_WHITELIST.contains(name)
  }
  if (hasBlacklist) {
    return !REPOSITORY_BLACKLIST.contains(name)
  }
  return true
}

Map<String, Map<String, Boolean>> storeRepositoryLookup = [:].withDefault { [:] }

repository.getRepositoryManager().browse().each { repo ->
  def blobStoreName = repo.properties.configuration.attributes.storage.blobStoreName
  storeRepositoryLookup.get(blobStoreName).put(repo.name, passesWhiteBlackList(repo.name))
}

blobStore.getBlobStoreManager().browse().each { blobstore ->
  //check that this blobstore is not a group (3.15.0+)
  if (blobstore.getProperties().getOrDefault('groupable',true)) {
    //S3 stores currently cannot be analysed via this script, so ignore (3.12.0+)
    if (blobstore.getProperties().get("blobStoreConfiguration").type == "S3") {
      log.info("Ignoring blobstore {} as it is using S3",
          blobstore.getProperties().get("blobStoreConfiguration").name);
    }
    else {
      try {
        blobstoreName = blobstore.getProperties().get("blobStoreConfiguration").name
        blobStoreDirectories[blobstoreName] = blobstore.getProperties().get("absoluteBlobDir").toFile()
      }
      catch (Exception ex) {
        log.warn('Unable to add blobstore {} of type {}: {}',
            blobstore.getProperties().get("blobStoreConfiguration").name,
            blobstore.getProperties().get("blobStoreConfiguration").type, ex.getMessage())
        log.info('details: {}', blobstore.getProperties())
      }
    }
  }
  else {
    log.info("Ignoring blobstore {} as it is a group store",
        blobstore.getProperties().get("blobStoreConfiguration").name);
  }
}

log.info('Blob Storage scan STARTED.')
blobStoreDirectories.each { blobStore ->
  Path contentDir = blobStore.value.toPath().resolve('content')
  log.info('Scanning blobstore {}, root dir {}, content dir {}', blobStore.key, blobStore.value.absolutePath, contentDir)

  BlobStatistics blobStat = new BlobStatistics()

  Set<String> unmapped = new HashSet<>()
  storeRepositoryLookup[blobStore.value.getName()].each { key, value ->
    if (value) {
      blobStat.repositories.put(key, new RepoStatistics())
    } else {
      unmapped.add(key)
    }
  }

  def blobstoreDir = new File(blobStore.value.path)
  def includePattern = "glob:**${SEP}${blobstoreDir.getName()}${SEP}content${SEP}**${SEP}*.properties"
  PathMatcher INCLUDE_MATCHER = FileSystems.getDefault().getPathMatcher(includePattern)
  log.info("Looking for blob properties files matching: ${includePattern}")
  contentDir.eachFileRecurse(FILES) { p ->
    if (!EXCLUDE_MATCHER.matches(p) && INCLUDE_MATCHER.matches(p) ) {
      File propertiesFile = p.toFile()
      def properties = new Properties()
      try {
        propertiesFile.withInputStream { is ->
          properties.load(is)
        }
      } catch (FileNotFoundException ex) {
        log.warn("File not found '{}', skipping", propertiesFile.getCanonicalPath())
      } catch (Exception e) {
        log.error('Unable to process {}', propertiesFile.getAbsolutePath(), e)
        throw e
      }
      collectMetrics(blobStat, unmapped, properties, propertiesFile)
    }
  }
  blobStatCollection.put(blobStore.value.getName(), blobStat)
}

def getMB(long value) {
    return (value/1024/1024).setScale(2, RoundingMode.HALF_UP)
}

def getGB(long value) {
    return (value/1024/1024/1024).setScale(2, RoundingMode.HALF_UP)
}

blobStatCollection.each() { blobStoreName, blobStat ->
  RepoStatistics directPath = blobStat.repositories.remove('SYSTEM:direct-path')
  if (directPath!=null) {
    log.info("Direct-Path size in blobstore {}: {} - reclaimable: {}", blobStoreName, directPath.totalBytes, directPath.reclaimableBytes)
  }
  blobStat.totalBlobStoreMB = getMB(blobStat.totalBlobStoreBytes)
  blobStat.totalBlobStoreGB = getGB(blobStat.totalBlobStoreBytes)
  blobStat.totalReclaimableMB = getMB(blobStat.totalReclaimableBytes)
  blobStat.totalReclaimableGB = getGB(blobStat.totalReclaimableBytes)
  blobStat.repositories = blobStat.repositories.toSorted { a, b -> b.value.totalBytes <=> a.value.totalBytes }
  blobStat.repositories.each() { k,v ->
    blobStat.repositories."$k".totalMB=getMB(v.totalBytes)
    blobStat.repositories."$k".totalGB=getGB(v.totalBytes)
    blobStat.repositories."$k".reclaimableMB=getMB(v.reclaimableBytes)
    blobStat.repositories."$k".reclaimableGB=getGB(v.reclaimableBytes)
  }  
}
def filename = "repoSizes-${new SimpleDateFormat("yyyyMMdd-HHmmss").format(new Date())}.json"
File resultsFile = new File(resultsFileLocation, filename)
resultsFile.withWriter { Writer writer ->
  writer << JsonOutput.prettyPrint(JsonOutput.toJson(blobStatCollection.findAll {a, b -> b.repositories.size() > 0}.toSorted {a, b -> b.value.totalBlobStoreBytes <=> a.value.totalBlobStoreBytes}))
}
log.info('Blob Storage scan ENDED. Report at {}', resultsFile.absolutePath)