FROM node:18.17.0-bullseye
ENV HUGO_VERSION=0.116.1
WORKDIR /app
RUN sed -i.bak "s,\(ca.archive\|archive\|security\).ubuntu.com,{{ param_mirror_apt }},g" /etc/apt/sources.list
RUN apt update -y && apt install wget -y
RUN wget -nv -O /tmp/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb && dpkg -i /tmp/hugo.deb