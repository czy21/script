# apt
```yaml
apt:
    apt-debian11-proxy:
      type: proxy
      distribution: bullseye
      proxy-url: http://mirrors.aliyun.com/debian/
    apt-debian11-proxy-security:
      type: proxy
      distribution: bullseye
      proxy-url: http://mirrors.aliyun.com/debian-security/
    apt-ubuntu18-proxy:
      type: proxy
      distribution: bionic
      proxy-url: http://mirrors.aliyun.com/ubuntu/
    apt-ubuntu20-proxy:
      type: proxy
      distribution: focal
      proxy-url: http://mirrors.aliyun.com/ubuntu/
go: 
  go-proxy:
    type: proxy
    proxy-url: https://goproxy.io
helm:
  helm-hosted:
    type: hosted
    deployment-policy: Allow
maven:
  maven-central:
    type: proxy
    proxy-url: https://repo1.maven.org/maven2/
    version-policy: Release
    layout-policy: Permissive
    content-isposition: Inline
  maven-releases:
    type: hosted
    version-policy: Release
    layout-policy: Strict
    content-isposition: Inline
    deployment-policy: Disable
  maven-snapshots:
    type: hosted
    version-policy: Snapshot
    layout-policy: Strict
    content-isposition: Inline
    deployment-policy: Allow
  maven-public:
    type: group
    version-policy: Release
    layout-policy: Strict
    content-isposition: Inline
    
pypi:
  pypi-proxy:
    type: proxy
    proxy-url: https://pypi.org
yum:
  yum-proxy:
    type: proxy
    proxy-url: http://mirror.centos.org/centos/
npm:
  npm-proxy:
    type: proxy
    proxy-url: https://registry.npmjs.org
nuget:
  nuget-hosted:
    type: hosted
    deployment-policy: Allow
  nuget.org-proxy:
    type: proxy
    protocal-version: Nuget V3
    proxy-url: https://api.nuget.org/v3/index.json
   nuget-group:
    type: group
```