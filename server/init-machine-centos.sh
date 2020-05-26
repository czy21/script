#!/bin/bash
#sh init-machine-centos.sh -h user@host -t ali local
# -t ali | offical local|remote
# must as root
set -e

while [[ $# -ge 1 ]]; do
  case $1 in
  -h)
    source ../utility/share.sh
    host=$2
    sh_file='init-machine-centos.sh'
    cp_path=$sh_file
    rm_path=$sh_file
    upload_exec $@
    shift 2
    break
    ;;
  -t)
    shift 1

    # install tools
    yum -y install wget vim

    # edit sshd_config
    sed -i -r "s/ll='ls\s+-l/\0va/" /etc/profile.d/colorls.sh
    sed -i -r "s/\s*#\s*(%wheel\s+ALL=\(ALL\)\s+ALL)/\1/" /etc/sudoers
    sed -i -r "s/^\s*UseDNS\s+\w+/#\0/; s/^\s*PermitRootLogin\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/" /etc/ssh/sshd_config
    echo "
      UseDNS no
      PermitRootLogin no
      PasswordAuthentication no
      ClientAliveInterval 30
      " >>/etc/ssh/sshd_config

    if [ $1 == 'ali' ]; then
      # use ali yum.repo
      sudo mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
      wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
      sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
      yum clean all
      yum makecache
    fi

    # add first user
    useradd -m bruce
    usermod -aG wheel bruce
    passwd -d bruce
    sudo -u bruce bash -c "set -e;cd;mkdir .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"

    if [ $2 == 'local' ]; then
      systemctl disable firewalld
      sed -i -r "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config
    fi

    shutdown -r now

    shift 2
    ;;
  *)
    echo -e "\033[31m$1 un_know input param \033[0m"
    break
    ;;
  esac
done
