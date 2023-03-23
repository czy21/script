FROM ubuntu:bionic

RUN sed -i.bak "s,\(ca.archive\|archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt-get update

RUN apt install -y sudo wget vim git bash-completion make gcc
RUN wget -O - https://raw.githubusercontent.com/friendlyarm/build-env-on-ubuntu-bionic/master/install.sh | bash
RUN apt-get clean

RUN useradd -d /home/{{ param_user_ops }} -l -m -s /bin/bash {{ param_user_ops }}
RUN su {{ param_user_ops }} bash -c 'git config --global user.email "{{ param_user_ops }}@localhost" && git config --global user.name "{{ param_user_ops }}"'
WORKDIR /data