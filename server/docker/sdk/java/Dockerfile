ARG BASE_IMAGE=eclipse-temurin:8u462-b08-jdk-noble

FROM $BASE_IMAGE

WORKDIR /app
ENV JAR=/app/api.jar

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080 9999
ENTRYPOINT ["/docker-entrypoint.sh"]