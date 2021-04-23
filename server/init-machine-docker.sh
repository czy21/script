#!/bin/bash
# bash init-machine-docker.sh -h user@host -t ali
# -t ali | offical
set -e

while getopts ":h:t:" opt
do
	case $opt in
  h)
      source ../utility/share.sh
      host=$2
      sh_file=$0
      shift 2
      upload_exec_sh $@
      break
			;;
	t)
	    shift 1
		  sudo mkdir -p /etc/docker
		  sudo mkdir -p /etc/systemd/system/docker.service.d/
      sudo tee /etc/systemd/system/docker.service.d/docker.conf <<-'EOF'
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd
EOF
      if [ $1 == 'ali' ]; then
        sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "data-root": "/volume1/docker-root",
  "hosts": ["fd://","tcp://0.0.0.0:2375"],
  "registry-mirrors": ["https://idyylogn.mirror.aliyuncs.com","https://registry.docker-cn.com"]
}
EOF
      fi
      if [ $1 == 'offical' ]; then
        sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "data-root": "/volume1/docker-root",
  "hosts": ["fd://","tcp://0.0.0.0:2375"]
}
EOF
      fi
      sudo yum install -y yum-utils
      sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
      sudo yum -y install docker-ce docker-ce-cli containerd.io
      sudo systemctl daemon-reload
      sudo systemctl restart docker
      sudo systemctl enable docker
      sudo docker network create local_default

      # docker compose
      sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose
      sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

      # docker machine
      sudo curl -L "https://github.com/docker/machine/releases/download/v0.16.0/docker-machine-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-machine
      sudo chmod +x /usr/local/bin/docker-machine
      sudo ln -sf /usr/local/bin/docker-machine /usr/bin/docker-machine
			;;
		?)
		echo -e "\033[31m$1 un_know input param \033[0m"
		break
		;;
	esac
done