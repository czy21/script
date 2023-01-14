FROM ubuntu:jammy

RUN sed -i.bak "s,\(ca.archive\|archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt-get update

RUN apt install -y openssh-server sudo net-tools vim git
RUN apt install -y build-essential clang flex g++ gawk gcc-multilib gettext git libncurses5-dev libssl-dev python3-distutils rsync unzip zlib1g-dev file wget qemu-utils
RUN sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
RUN echo 'UseDNS no \nPermitRootLogin yes \nPasswordAuthentication yes \nClientAliveInterval 30' >> /etc/ssh/sshd_config;
RUN useradd -m {{ param_user_ops }} -d /home/{{ param_user_ops }} -s /bin/bash;passwd -d {{ param_user_ops }};
RUN groupadd wheel
RUN echo '%wheel ALL=(ALL:ALL)  NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG wheel {{ param_user_ops }}
RUN su {{ param_user_ops }} bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo {{ param_user_ops_opsor_ssh_public_key }} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'


COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/data"]
EXPOSE 22
ENTRYPOINT ["/docker-entrypoint.sh"]