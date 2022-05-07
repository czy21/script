#!/bin/bash
set -e

sed -i "s|^mirrorlist=|#mirrorlist=|g; s|^#baseurl=http://mirror.centos.org|baseurl={{ param_vault_centos_proxy }}|g"  /etc/yum.repos.d/CentOS-*.repo

yum -y install wget vim git nfs-utils bash-completion
dnf -y install python38
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

useradd -m bruce
usermod -aG wheel bruce
passwd -d bruce

public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u root bash -c "${public_key}"
sudo -u bruce bash -c "${public_key}"

systemctl disable firewalld
sed -i -r "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config