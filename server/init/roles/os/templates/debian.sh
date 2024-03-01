#!/bin/bash
set -e

echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom

apt -y update
apt -y install wget vim git nfs-common cifs-utils make gcc iputils-ping bash-completion systemd-timesyncd rsync netcat curl

grep '{{ param_user_ops }}' /etc/passwd -q || useradd -m {{ param_user_ops }} -s /bin/bash
usermod -aG sudo {{ param_user_ops }}
public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_user_ops_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u {{ param_user_ops }} bash -c "${public_key}"

sudo -u root bash -c "${public_key}"