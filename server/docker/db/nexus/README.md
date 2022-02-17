# apt
```yaml
apt:
    apt-proxy-debian:
      type: proxy
      distribution: bullseye
      proxy-url: https://mirrors.aliyun.com/debian/
    apt-proxy-debian-security:
      type: proxy
      distribution: bullseye
      proxy-url: https://mirrors.aliyun.com/debian-security/
    apt-proxy-ubuntu:
      type: proxy
      distribution: focal
      proxy-url: https://mirrors.aliyun.com/ubuntu/
docker:
  docker-proxy-offical:
    type: proxy
    proxy-url: https://registry-1.docker.io
  docker-proxy-quay:
    type: proxy
    proxy-url: https://quay.io
  docker-proxy-gcr:
    type: proxy
    proxy-url: https://gcr.io
  docker-proxy-mcr:
    type: proxy
    proxy-url: https://mcr.microsoft.com
  docker-proxy-k8s:
    type: proxy
    proxy-url: https://k8s.gcr.io
  docker-proxy-es:
    type: proxy
    proxy-url: https://docker.elastic.co
  
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
    proxy-url: https://mirror.centos.org/centos/
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