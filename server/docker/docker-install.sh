#!/bin/bash
#sh docker-install -h user@host -t ali
# -t ali | offical
set -e

if [ $1 == '-h' ]; then
  if [[ ! $2 ]] || [[ "$2" =~ ^"-".* ]]; then
    echo -e "\033[31m$1 value is null \033[0m"
    shift 1
    continue
  fi
  host=$2
  shift 2
  scp -r docker-install.sh $host:
  ssh $host '$HOME/docker-install.sh '$@';'
  ssh $host 'rm -rf $HOME/docker-install.sh'
  exit
fi

sudo mkdir -p /data/config/ /data/volumes/

# 初始化目标源
while [[ $# -ge 1 ]]; do
  case $1 in
  -t)
    if [[ ! $2 ]] || [[ "$2" =~ ^"-".* ]]; then
      echo -e "\033[31m$1 value is null \033[0m"
      shift 1
      continue
    fi
    shift 1
    if [ $1 == 'ali' ]; then
      sudo mkdir -p /etc/docker
      sudo tee /etc/docker/daemon.json <<-'EOF'
      {
        "registry-mirrors": ["https://idyylogn.mirror.aliyuncs.com"]
      }
      EOF
      sudo yum install -y yum-utils device-mapper-persistent-data lvm2
      sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
      sudo yum makecache timer
      sudo yum -y install docker-ce
      sudo systemctl daemon-reload
    fi
    if [ $1 == 'offical' ]; then
      sudo yum install -y yum-utils
      sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
      sudo yum -y install docker-ce docker-ce-cli containerd.io
    fi
    break
    ;;
  *)
    echo -e "\033[31m$1 un_know input param \033[0m"
    break
    ;;
  esac
done

sudo systemctl restart docker
sudo systemctl enable docker

# docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# docker machine
sudo curl -L "https://github.com/docker/machine/releases/download/v0.16.0/docker-machine-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-machine
sudo chmod +x /usr/local/bin/docker-machine
sudo ln -sf /usr/local/bin/docker-machine /usr/bin/docker-machine
