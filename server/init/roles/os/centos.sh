#!/bin/bash
set -e

echo centos

# yum -y install wget vim git nfs-utils bash-completion
# dnf -y install python38
# sed -i -r "s/ll='ls\s+-l/\0va/" /etc/profile.d/colorls.sh
# sed -i -r "s/\s*#\s*(%wheel\s+ALL=\(ALL\)\s+ALL)/\1/" /etc/sudoers
# sed -i -r "s/^\s*UseDNS\s+\w+/#\0/; s/^\s*PermitRootLogin\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/" /etc/ssh/sshd_config
# echo "
# UseDNS no
# PermitRootLogin yes
# PasswordAuthentication no
# ClientAliveInterval 30
# " >>/etc/ssh/sshd_config

# yum clean all
# yum makecache

# useradd -m bruce
# usermod -aG wheel bruce
# passwd -d bruce

# public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
# sudo -u root bash -c "${public_key}"
# sudo -u bruce bash -c "${public_key}"

# systemctl disable firewalld
# sed -i -r "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config