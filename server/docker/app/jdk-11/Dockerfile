FROM openjdk:11-jre-slim
WORKDIR /home/app

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ENV JAR=/home/app/api.jar

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/home/app/config/","/home/app/data/"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]