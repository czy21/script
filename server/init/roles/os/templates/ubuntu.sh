#!/bin/bash
set -e

sed -i.bak "s,\(ca.archive\|archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list

apt -y update
apt -y install wget vim git network-manager nfs-common make gcc python3-pip

# postgres repo
#sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
#wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# install optional
#apt -y install mysql-client postgresql-client

sed -i -r "s/^\s*%sudo.*/%sudo   ALL=(ALL:ALL) NOPASSWD:ALL/;" /etc/sudoers

sed -i -r "s/^\s*UseDNS\s+\w+/#\0/; s/^\s*PermitRootLogin\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/" /etc/ssh/sshd_config
echo "
UseDNS no
PermitRootLogin yes
PasswordAuthentication no
ClientAliveInterval 30
" >>/etc/ssh/sshd_config

public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u root bash -c "${public_key}"
sudo -u bruce bash -c "${public_key}"

ufw disable

swapoff -a
sed -i -r "s/^\s*/swap.img\s+\w+/#\0/" /etc/fstab