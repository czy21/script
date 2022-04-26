# apt

```json
{
  "apt": [
    {
      "name": "apt-proxy-debian",
      "url": "http://nexus.cluster.com/repository/apt-proxy-debian",
      "apt": {
        "distribution": "bullseye",
        "flat": false
      },
      "proxy": {
        "remoteUrl": "https://mirrors.aliyun.com/debian/"
      },
      "type": "proxy"
    },
    {
      "name": "apt-proxy-debian-security",
      "url": "http://nexus.cluster.com/repository/apt-proxy-debian-security",
      "apt": {
        "distribution": "bullseye",
        "flat": false
      },
      "proxy": {
        "remoteUrl": "https://mirrors.aliyun.com/debian-security/"
      },
      "type": "proxy"
    },
    {
      "name": "apt-proxy-ubuntu",
      "url": "http://nexus.cluster.com/repository/apt-proxy-ubuntu",
      "apt": {
        "distribution": "focal",
        "flat": false
      },
      "proxy": {
        "remoteUrl": "https://mirrors.aliyun.com/ubuntu/"
      },
      "type": "proxy"
    }
  ],
  "docker": [
    {
      "name": "docker-proxy-group",
      "url": "http://nexus.cluster.com/repository/docker-proxy-group",
      "group": {
        "memberNames": [
          "docker-proxy-official",
          "docker-proxy-gcr",
          "docker-proxy-quay",
          "docker-proxy-mcr",
          "docker-proxy-k8s",
          "docker-proxy-es"
        ]
      },
      "type": "group"
    },
    {
      "name": "docker-hosted",
      "url": "http://nexus.cluster.com/repository/docker-hosted",
      "type": "hosted"
    },
    {
      "name": "docker-proxy-es",
      "url": "http://nexus.cluster.com/repository/docker-proxy-es",
      "dockerProxy": {
        "indexType": "REGISTRY",
        "indexUrl": null
      },
      "proxy": {
        "remoteUrl": "https://docker.elastic.co"
      },
      "type": "proxy"
    },
    {
      "name": "docker-proxy-gcr",
      "url": "http://nexus.cluster.com/repository/docker-proxy-gcr",
      "dockerProxy": {
        "indexType": "REGISTRY",
        "indexUrl": null
      },
      "proxy": {
        "remoteUrl": "https://gcr.io"
      },
      "type": "proxy"
    },
    {
      "name": "docker-proxy-k8s",
      "url": "http://nexus.cluster.com/repository/docker-proxy-k8s",
      "dockerProxy": {
        "indexType": "REGISTRY",
        "indexUrl": null
      },
      "proxy": {
        "remoteUrl": "https://k8s.gcr.io"
      },
      "type": "proxy"
    },
    {
      "name": "docker-proxy-mcr",
      "url": "http://nexus.cluster.com/repository/docker-proxy-mcr",
      "dockerProxy": {
        "indexType": "REGISTRY",
        "indexUrl": null
      },
      "proxy": {
        "remoteUrl": "https://mcr.microsoft.com"
      },
      "type": "proxy"
    },
    {
      "name": "docker-proxy-official",
      "url": "http://nexus.cluster.com/repository/docker-proxy-official",
      "dockerProxy": {
        "indexType": "HUB",
        "indexUrl": null
      },
      "proxy": {
        "remoteUrl": "https://registry-1.docker.io"
      },
      "type": "proxy"
    },
    {
      "name": "docker-proxy-quay",
      "url": "http://nexus.cluster.com/repository/docker-proxy-quay",
      "dockerProxy": {
        "indexType": "REGISTRY",
        "indexUrl": null
      },
      "proxy": {
        "remoteUrl": "https://quay.io"
      },
      "type": "proxy"
    }
  ],
  "go": [
    {
      "name": "go-proxy",
      "url": "http://nexus.cluster.com/repository/go-proxy",
      "proxy": {
        "remoteUrl": "https://goproxy.io"
      },
      "type": "proxy"
    }
  ],
  "helm": [
    {
      "name": "helm-hosted",
      "url": "http://nexus.cluster.com/repository/helm-hosted",
      "type": "hosted"
    }
  ],
  "maven2": [
    {
      "name": "maven-public",
      "url": "http://nexus.cluster.com/repository/maven-public",
      "group": {
        "memberNames": [
          "maven-releases",
          "maven-snapshots",
          "maven-proxy-central",
          "maven-proxy-gradle"
        ]
      },
      "type": "group"
    },
    {
      "name": "maven-releases",
      "url": "http://nexus.cluster.com/repository/maven-releases",
      "maven": {
        "versionPolicy": "RELEASE",
        "layoutPolicy": "STRICT",
        "contentDisposition": null
      },
      "type": "hosted"
    },
    {
      "name": "maven-snapshots",
      "url": "http://nexus.cluster.com/repository/maven-snapshots",
      "maven": {
        "versionPolicy": "SNAPSHOT",
        "layoutPolicy": "STRICT",
        "contentDisposition": null
      },
      "type": "hosted"
    },
    {
      "name": "maven-proxy-central",
      "url": "http://nexus.cluster.com/repository/maven-proxy-central",
      "proxy": {
        "remoteUrl": "https://maven.aliyun.com/repository/central"
      },
      "maven": {
        "versionPolicy": "RELEASE",
        "layoutPolicy": "PERMISSIVE",
        "contentDisposition": "INLINE"
      },
      "type": "proxy"
    },
    {
      "name": "maven-proxy-gradle",
      "url": "http://nexus.cluster.com/repository/maven-proxy-gradle",
      "proxy": {
        "remoteUrl": "https://maven.aliyun.com/repository/gradle-plugin"
      },
      "maven": {
        "versionPolicy": "RELEASE",
        "layoutPolicy": "PERMISSIVE",
        "contentDisposition": "INLINE"
      },
      "type": "proxy"
    }
  ],
  "npm": [
    {
      "name": "npm-group",
      "url": "http://nexus.cluster.com/repository/npm-group",
      "group": {
        "memberNames": [
          "npm-hosted",
          "npm-proxy"
        ]
      },
      "type": "group"
    },
    {
      "name": "npm-hosted",
      "url": "http://nexus.cluster.com/repository/npm-hosted",
      "type": "hosted"
    },
    {
      "name": "npm-proxy",
      "url": "http://nexus.cluster.com/repository/npm-proxy",
      "proxy": {
        "remoteUrl": "https://registry.npmjs.org"
      },
      "npm": {
        "removeNonCataloged": false,
        "removeQuarantined": false
      },
      "type": "proxy"
    }
  ],
  "nuget": [
    {
      "name": "nuget-group",
      "url": "http://nexus.cluster.com/repository/nuget-group",
      "group": {
        "memberNames": [
          "nuget-hosted",
          "nuget.org-proxy"
        ]
      },
      "type": "group"
    },
    {
      "name": "nuget-hosted",
      "url": "http://nexus.cluster.com/repository/nuget-hosted",
      "type": "hosted"
    },
    {
      "name": "nuget.org-proxy",
      "url": "http://nexus.cluster.com/repository/nuget.org-proxy",
      "proxy": {
        "remoteUrl": "https://api.nuget.org/v3/index.json"
      },
      "nugetProxy": {
        "queryCacheItemMaxAge": 3600,
        "nugetVersion": "V3"
      },
      "type": "proxy"
    }
  ],
  "pypi": [
    {
      "name": "pypi-proxy",
      "url": "http://nexus.cluster.com/repository/pypi-proxy",
      "proxy": {
        "remoteUrl": "https://pypi.org"
      },
      "type": "proxy"
    }
  ],
  "yum": [
    {
      "name": "yum-proxy",
      "url": "http://nexus.cluster.com/repository/yum-proxy",
      "proxy": {
        "remoteUrl": "https://mirrors.aliyun.com/centos-vault/"
      },
      "type": "proxy"
    }
  ]
}
```