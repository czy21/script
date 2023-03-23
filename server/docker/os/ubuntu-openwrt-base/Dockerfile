FROM ubuntu:jammy

RUN sed -i.bak "s,\(ca.archive\|archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt-get update

RUN apt install -y wget vim git bash-completion make gcc

RUN useradd -d /home/{{ param_user_ops }} -l -m -s /bin/bash {{ param_user_ops }}

WORKDIR /data