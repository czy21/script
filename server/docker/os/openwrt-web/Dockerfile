FROM nginx:1.29.0-alpine-perl

RUN apk add --no-cache fcgiwrap spawn-fcgi perl-json

COPY 99-docker-entrypoint-fcgiwrap.sh /docker-entrypoint.d