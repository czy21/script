FROM debian:buster

RUN sed -i.bak "s,\(security\|deb\).debian.org,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt-get update && apt-get clean