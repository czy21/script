FROM jenkins/inbound-agent:alpine-jdk11
USER root

RUN apk update;
RUN apk add wget vim;

RUN wget -O - https://get.helm.sh/helm-v3.6.3-linux-amd64.tar.gz | tar -zxf - --strip-components 1 -C /usr/local/bin/ linux-amd64/helm
RUN chmod +x /usr/local/bin/helm
RUN ln -s /usr/local/bin/helm /usr/bin/helm