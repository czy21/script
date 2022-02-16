# apt
```yaml
apt:
    apt-debian11-proxy:
      distribution: bullseye
      proxy-url: http://mirrors.aliyun.com/debian/
    apt-debian11-proxy-security:
      distribution: bullseye
      proxy-url: http://mirrors.aliyun.com/debian-security/
    apt-ubuntu18-proxy:
      distribution: bionic
      proxy-url: http://mirrors.aliyun.com/ubuntu/
    apt-ubuntu20-proxy:
      distribution: focal
      proxy-url: http://mirrors.aliyun.com/ubuntu/
go: 
  go-proxy:
    proxy-url: https://goproxy.io
maven:
  maven-central:
    proxy-url: https://repo1.maven.org/maven2/
pypi:
  pypi-proxy:
    proxy-url: https://pypi.org
yum:
  yum-proxy:
    proxy-url: http://mirror.centos.org/centos/
```