FROM eclipse-temurin:21.0.1_12-jdk-jammy

WORKDIR /app
ENV JAR=/app/api.jar

RUN mkdir conf

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/app/data/","/app/log"]
EXPOSE 8080 9999
ENTRYPOINT ["/docker-entrypoint.sh"]