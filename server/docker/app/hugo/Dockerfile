FROM node:18.17.0-bullseye
ARG HUGO_VERSION=0.117.0

LABEL org.opencontainers.image.url='https://github.com/czy21/container'
LABEL org.opencontainers.image.source='https://github.com/czy21/container/tree/main/hugo'
LABEL org.opencontainers.image.title='based on node:18.17.0-bullseye'
LABEL org.opencontainers.image.authors='a805899926@gmail.com>'

WORKDIR /app

RUN apt-get update -y && apt install wget -y && rm -rf /var/lib/apt/lists/*
RUN wget -nv -O /tmp/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb && dpkg -i /tmp/hugo.deb