#!/bin/bash
set -e

echo -n "%wheel ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom

yum clean all && yum --refresh makecache

yum -y install tar wget vim nfs-utils bash-completion git jq rsync nc net-tools

if [ "centos" == "{{ param_ansible_distribution }}" ];then
  dnf -y install python39
fi

grep '{{ param_user_ops }}' /etc/passwd -q || useradd -m {{ param_user_ops }} && usermod -aG wheel {{ param_user_ops }} && passwd -d {{ param_user_ops }} && chown {{ param_user_ops }}:{{ param_user_ops }} /home/{{ param_user_ops }}

public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_user_ops_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u root bash -c "${public_key}"
sudo -u {{ param_user_ops }} bash -c "${public_key}"

systemctl stop firewalld && systemctl disable firewalld

setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

# fix: Missing privilege separation directory: /run/sshd
echo 'd /var/run/sshd 0755 root' > /usr/lib/tmpfiles.d/sshd.conf

# fedora disable swap
if [ "fedora" == "{{ param_ansible_distribution }}" ];then
  systemctl mask systemd-zram-setup@zram0
fi