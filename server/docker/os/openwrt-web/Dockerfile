FROM nginx:1.28.0-alpine

RUN apk add --no-cache fcgiwrap spawn-fcgi perl perl-cgi

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]