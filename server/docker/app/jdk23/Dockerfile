FROM eclipse-temurin:23.0.1_11-jdk-noble

WORKDIR /app
ENV JAR=/app/api.jar

RUN mkdir conf

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/app/data/","/app/log"]
EXPOSE 8080 9999
ENTRYPOINT ["/docker-entrypoint.sh"]