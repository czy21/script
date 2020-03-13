#!/bin/bash

sudo docker run -i -d --name ubuntu_one -p 4022:22 ubuntu:18.04

sudo docker exec -i ubuntu_one /bin/bash -c "
sed -i 's/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list;
apt-get update;
apt install -y openssh-client openssh-server subversion g++ zlib1g-dev build-essential git python rsync man-db;
apt install -y libncurses5-dev gawk gettext unzip file libssl-dev wget zip time vim sudo nscd;
useradd -m bruce -d /home/bruce -s /bin/bash;passwd -d bruce;
sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PermitRootLogin\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
echo '
UseDNS no
PermitRootLogin yes
PasswordAuthentication yes
ClientAliveInterval 30
' >> /etc/ssh/sshd_config;
/etc/init.d/ssh start;
su bruce bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'
"