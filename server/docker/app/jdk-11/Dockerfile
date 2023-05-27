FROM openjdk:11.0.16-jdk-bullseye
WORKDIR /app

ENV JAR=/app/api.jar

RUN mkdir conf

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/app/data/","/app/log"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]