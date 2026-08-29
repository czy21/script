#!/bin/bash
set -e

echo "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom

grep -q '{{ param_user }}' /etc/passwd || useradd -m {{ param_user }} -s /bin/bash && chown {{ param_user }}:{{ param_user }} /home/{{ param_user }} && usermod -aG sudo {{ param_user }}
public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_user_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
su {{ param_user }} bash -c "${public_key}"

NEEDRESTART_SUSPEND=1 apt-get remove needrestart -y && apt-get autoclean -y && apt-get autoremove -y

apt-get -y update
apt-get -y install ca-certificates lsb-release curl wget vim git nfs-common cifs-utils net-tools make gcc iputils-ping bash-completion systemd-timesyncd systemd-resolved rsync ncdu nload

# fix: Missing privilege separation directory: /run/sshd
echo 'd /var/run/sshd 0755 root' > /usr/lib/tmpfiles.d/sshd.conf

swapoff -a
sed -i -r "s|^/swap.img|#\0|" /etc/fstab