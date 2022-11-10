#!/bin/bash
set -e

yum clean all && yum --refresh makecache

yum -y install wget vim nfs-utils bash-completion git
dnf -y install python39

sed -i -r "s/ll='ls\s+-l/\0va/" /etc/profile.d/colorls.sh
sed -i -r "s/\s*#\s*(%wheel\s+ALL=\(ALL\)\s+ALL)/\1/" /etc/sudoers
sed -i -r "s/^\s*UseDNS\s+\w+/#\0/; s/^\s*PermitRootLogin\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/" /etc/ssh/sshd_config
echo "
UseDNS no
PermitRootLogin yes
PasswordAuthentication no
ClientAliveInterval 30
" >>/etc/ssh/sshd_config

useradd -m {{ param_user_ops }} && usermod -aG wheel {{ param_user_ops }} && passwd -d {{ param_user_ops }}

public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u root bash -c "${public_key}"
sudo -u {{ param_user_ops }} bash -c "${public_key}"

systemctl stop firewalld && systemctl disable firewalld
sed -i -r "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config