FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

RUN apt-get update;
RUN apt-get install -y openssh-server sudo net-tools vim git;
# lede dependency
RUN sudo apt-get -y install build-essential asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch python3 python2.7 unzip zlib1g-dev lib32gcc1 libc6-dev-i386 subversion flex uglifyjs git-core gcc-multilib p7zip p7zip-full msmtp libssl-dev texinfo libglib2.0-dev xmlto qemu-utils upx libelf-dev autoconf automake libtool autopoint device-tree-compiler g++-multilib antlr3 gperf wget curl swig rsync
RUN sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
RUN echo 'UseDNS no \nPermitRootLogin yes \nPasswordAuthentication yes \nClientAliveInterval 30' >> /etc/ssh/sshd_config;
RUN cat /etc/ssh/sshd_config
RUN useradd -m {{ param_user_ops }} -d /home/{{ param_user_ops }} -s /bin/bash;passwd -d {{ param_user_ops }};
RUN groupadd wheel
RUN echo '%wheel ALL=(ALL:ALL)  NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG wheel {{ param_user_ops }}
RUN su {{ param_user_ops }} bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo {{ param_user_ops_opsor_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'

EXPOSE 22
ENTRYPOINT ["/docker-entrypoint.sh"]