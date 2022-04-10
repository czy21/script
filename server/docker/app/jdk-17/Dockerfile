FROM openjdk:17-slim
WORKDIR /app

ENV JAR=/app/api.jar

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/app/conf/","/app/data/"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]