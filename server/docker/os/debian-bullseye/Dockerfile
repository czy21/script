FROM debian:bullseye

RUN sed -i "s,\(security\|deb\).debian.org,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt-get update && apt-get clean