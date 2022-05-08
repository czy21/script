# apt

```json
{
  "apt": [
    {
      "name": "apt-proxy-debian",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/apt-proxy-debian",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://mirrors.aliyun.com/debian/"
        }
      }
    },
    {
      "name": "apt-proxy-debian-security",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/apt-proxy-debian-security",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://mirrors.aliyun.com/debian-security/"
        }
      }
    },
    {
      "name": "apt-proxy-ubuntu",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/apt-proxy-ubuntu",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://mirrors.aliyun.com/ubuntu/"
        }
      }
    }
  ],
  "docker": [
    {
      "name": "docker-proxy-group",
      "type": "group",
      "url": "http://nexus.cluster.com/repository/docker-proxy-group",
      "attributes": {}
    },
    {
      "name": "docker-hosted",
      "type": "hosted",
      "url": "http://nexus.cluster.com/repository/docker-hosted",
      "attributes": {}
    },
    {
      "name": "docker-proxy-es",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/docker-proxy-es",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://docker.elastic.co"
        }
      }
    },
    {
      "name": "docker-proxy-gcr",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/docker-proxy-gcr",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://gcr.io"
        }
      }
    },
    {
      "name": "docker-proxy-k8s",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/docker-proxy-k8s",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://k8s.gcr.io"
        }
      }
    },
    {
      "name": "docker-proxy-mcr",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/docker-proxy-mcr",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://mcr.microsoft.com"
        }
      }
    },
    {
      "name": "docker-proxy-official",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/docker-proxy-official",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://registry-1.docker.io"
        }
      }
    },
    {
      "name": "docker-proxy-quay",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/docker-proxy-quay",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://quay.io"
        }
      }
    }
  ],
  "go": [
    {
      "name": "go-proxy",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/go-proxy",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://goproxy.io"
        }
      }
    }
  ],
  "helm": [
    {
      "name": "helm-hosted",
      "type": "hosted",
      "url": "http://nexus.cluster.com/repository/helm-hosted",
      "attributes": {}
    }
  ],
  "maven2": [
    {
      "name": "maven-public",
      "type": "group",
      "url": "http://nexus.cluster.com/repository/maven-public",
      "attributes": {}
    },
    {
      "name": "maven-releases",
      "type": "hosted",
      "url": "http://nexus.cluster.com/repository/maven-releases",
      "attributes": {}
    },
    {
      "name": "maven-snapshots",
      "type": "hosted",
      "url": "http://nexus.cluster.com/repository/maven-snapshots",
      "attributes": {}
    },
    {
      "name": "maven-central",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/maven-central",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://repo1.maven.org/maven2/"
        }
      }
    },
    {
      "name": "maven-proxy-gradle",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/maven-proxy-gradle",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://plugins.gradle.org/m2/"
        }
      }
    }
  ],
  "npm": [
    {
      "name": "npm-group",
      "type": "group",
      "url": "http://nexus.cluster.com/repository/npm-group",
      "attributes": {}
    },
    {
      "name": "npm-hosted",
      "type": "hosted",
      "url": "http://nexus.cluster.com/repository/npm-hosted",
      "attributes": {}
    },
    {
      "name": "npm-proxy",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/npm-proxy",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://registry.npmjs.org"
        }
      }
    }
  ],
  "nuget": [
    {
      "name": "nuget-group",
      "type": "group",
      "url": "http://nexus.cluster.com/repository/nuget-group",
      "attributes": {}
    },
    {
      "name": "nuget-hosted",
      "type": "hosted",
      "url": "http://nexus.cluster.com/repository/nuget-hosted",
      "attributes": {}
    },
    {
      "name": "nuget.org-proxy",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/nuget.org-proxy",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://api.nuget.org/v3/index.json"
        }
      }
    }
  ],
  "pypi": [
    {
      "name": "pypi-proxy",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/pypi-proxy",
      "attributes": {
        "proxy": {
          "remoteUrl": "https://pypi.org"
        }
      }
    }
  ],
  "yum": [
    {
      "name": "yum-proxy-group",
      "type": "group",
      "url": "http://nexus.cluster.com/repository/yum-proxy-group",
      "attributes": {}
    },
    {
      "name": "yum-proxy-centos",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/yum-proxy-centos",
      "attributes": {
        "proxy": {
          "remoteUrl": "http://mirrors.aliyun.com/"
        }
      }
    },
    {
      "name": "yum-proxy-centos-vault",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/yum-proxy-centos-vault",
      "attributes": {
        "proxy": {
          "remoteUrl": "http://mirrors.aliyun.com/centos-vault/"
        }
      }
    },
    {
      "name": "yum-proxy-docker",
      "type": "proxy",
      "url": "http://nexus.cluster.com/repository/yum-proxy-docker",
      "attributes": {
        "proxy": {
          "remoteUrl": "http://download.docker.com/linux/"
        }
      }
    }
  ]
}
```