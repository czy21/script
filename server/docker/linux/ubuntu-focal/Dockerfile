FROM ubuntu:focal

RUN sed -i "s/archive.ubuntu.com\\/ubuntu/nexus.cluster.com\\/repository\\/apt-proxy-ubuntu\\//g" /etc/apt/sources.list
RUN apt-get update && apt-get clean