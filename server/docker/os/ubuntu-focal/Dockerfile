FROM ubuntu:focal

RUN sed -i "s,\(archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt-get update && apt-get clean