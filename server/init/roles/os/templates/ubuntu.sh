#!/bin/bash
set -e

sudo sed -i.bak "s,\(ca.archive\|jp.archive\|us.archive\|archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list

sudo NEEDRESTART_SUSPEND=1 apt remove needrestart -y && sudo apt autoclean -y && sudo apt autoremove -y

sudo apt -y update
sudo apt -y install wget vim git network-manager nfs-common make gcc iputils-ping bash-completion systemd-timesyncd

# postgres repo
#sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
#wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# install optional
#apt -y install mysql-client postgresql-client

sudo sed -i 's|^%sudo.*|%sudo   ALL=(ALL:ALL) NOPASSWD:ALL|g' /etc/sudoers

sudo sed -i -r \
-e 's/^\s*UseDNS\s+\w+/#\0/' \
-e 's/^\s*PermitRootLogin\s+\w+/#\0/' \
-e 's/^\s*PasswordAuthentication\s+\w+/#\0/' \
-e 's/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config

sudo -u root bash -c 'echo "
UseDNS no
PermitRootLogin yes
PasswordAuthentication no
ClientAliveInterval 30
" >> /etc/ssh/sshd_config'

public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo {{ param_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo -u {{ param_user_ops }} bash -c "${public_key}"