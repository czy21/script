FROM openjdk:17.0.2-jdk-bullseye
WORKDIR /app

ENV JAR=/app/api.jar

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/app/conf/","/app/data/"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]