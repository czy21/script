FROM node:14.17

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

#ENTRYPOINT ["/docker-entrypoint.sh"]