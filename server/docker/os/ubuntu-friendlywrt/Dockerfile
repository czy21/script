FROM ubuntu:bionic

RUN sed -i.bak "s,\(ca.archive\|archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt-get update

RUN apt install -y sudo net-tools wget vim git bash-completion make gcc
RUN wget -O - https://raw.githubusercontent.com/friendlyarm/build-env-on-ubuntu-bionic/master/install.sh | bash
RUN apt-get clean
RUN useradd -m {{ param_user_ops }} -d /home/{{ param_user_ops }} -s /bin/bash;passwd -d {{ param_user_ops }};
RUN groupadd wheel
RUN echo '%wheel ALL=(ALL:ALL)  NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG wheel {{ param_user_ops }}
RUN su {{ param_user_ops }} bash -c 'git config --global user.email "you@example.com" && git config --global user.name "{{ param_user_ops }}"'

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

WORKDIR /data

VOLUME ["/data"]
EXPOSE 22
ENTRYPOINT ["/docker-entrypoint.sh"]