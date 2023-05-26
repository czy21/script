#!/bin/bash
set -e

echo -n "%wheel  ALL=(ALL)       ALL" > /etc/sudoers.d/99-custom

yum clean all && yum --refresh makecache -v

yum -y install wget vim nfs-utils bash-completion git jq rsync nc net-tools
dnf -y install python39

useradd -m {{ param_user_ops }} && usermod -aG wheel {{ param_user_ops }} && passwd -d {{ param_user_ops }} && chown {{ param_user_ops }}:{{ param_user_ops }} /home/{{ param_user_ops }}

public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_user_ops_opsor_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u root bash -c "${public_key}"
sudo -u {{ param_user_ops }} bash -c "${public_key}"

systemctl stop firewalld && systemctl disable firewalld
sed -i -r "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config