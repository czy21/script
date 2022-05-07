FROM debian:bullseye

RUN sed -i "s/deb.debian.org\\/debian/nexus.cluster.com\\/repository\\/apt-proxy\\/debian\\//g" /etc/apt/sources.list
RUN sed -i "s/security.debian.org\\/debian-security/nexus.cluster.com\\/repository\\/apt-proxy\\/debian-security\\//g" /etc/apt/sources.list
RUN apt-get update && apt-get clean