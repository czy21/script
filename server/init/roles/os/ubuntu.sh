#!/bin/bash
set -e

echo ubuntu

# apt -y update
# apt -y install wget vim git network-manager nfs-common python3-pip

# # postgres repo
# # sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
# # wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# # install optional
# # apt -y install mysql-client postgresql-client

# sed -i -r "s/^\s*%sudo.*/%sudo   ALL=(ALL:ALL) NOPASSWD:ALL/;" /etc/sudoers

# sed -i -r "s/^\s*UseDNS\s+\w+/#\0/; s/^\s*PermitRootLogin\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/" /etc/ssh/sshd_config
# echo "
# UseDNS no
# PermitRootLogin yes
# PasswordAuthentication no
# ClientAliveInterval 30
# " >>/etc/ssh/sshd_config

# public_key="set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
# sudo -u root bash -c "${public_key}"
# sudo -u bruce bash -c "${public_key}"

# ufw disable