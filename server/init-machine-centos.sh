#!/bin/bash
# bash init-machine-centos.sh -h user@host -t
# must as root
set -e

while getopts ":h:t" opt
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
    timedatectl set-timezone Asia/Shanghai
    # install tools
    yum -y install wget
    dnf -y install python38
    # edit sshd_config
    sed -i -r "s/ll='ls\s+-l/\0va/" /etc/profile.d/colorls.sh
    sed -i -r "s/\s*#\s*(%wheel\s+ALL=\(ALL\)\s+ALL)/\1/" /etc/sudoers
    sed -i -r "s/^\s*UseDNS\s+\w+/#\0/; s/^\s*PermitRootLogin\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/" /etc/ssh/sshd_config
    echo "
      UseDNS no
      PermitRootLogin yes
      PasswordAuthentication no
      ClientAliveInterval 30
      " >>/etc/ssh/sshd_config

    yum clean all
    yum makecache

    # add first user
    useradd -m bruce
    usermod -aG wheel bruce
    passwd -d bruce
    sudo -u root bash -c "set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
    sudo -u bruce bash -c "set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"

    systemctl disable firewalld
    sed -i -r "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config

    yum -y install vim git

    shutdown -r now
		;;
		?)
		echo -e "\033[31m$1 un_know input param \033[0m"
		break
		;;
	esac
done
