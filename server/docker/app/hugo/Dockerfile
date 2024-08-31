FROM node:18.17.0-bullseye-slim
ARG HUGO_VERSION=0.117.0

WORKDIR /app

RUN apt-get update -y && apt install wget -y && rm -rf /var/lib/apt/lists/*
RUN wget -nv -O /tmp/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb && dpkg -i /tmp/hugo.deb