FROM openjdk:11.0.10-jre
WORKDIR /home/app

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ENV JAR=/home/app/api.jar
ENV CONFIG_DIR=/home/app/config/
ENV DATA_DIR=/home/app/data/

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["${CONFIG_DIR}","${DATA_DIR}"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]