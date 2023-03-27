#!/bin/bash
set -e

echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom

NEEDRESTART_SUSPEND=1 apt remove needrestart -y && apt autoclean -y && apt autoremove -y

apt -y update
apt -y install wget vim git nfs-common cifs-utils make gcc iputils-ping bash-completion systemd-timesyncd rsync netcat

# postgres repo
#sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
#wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# install optional
#apt -y install mysql-client postgresql-client

public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_user_ops_opsor_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u {{ param_user_ops }} bash -c "${public_key}"

swapoff -a
sed -i -r "s|^/swap.img|#\0|" /etc/fstab