FROM eclipse-temurin:21.0.2_13-jdk-jammy

WORKDIR /app
ENV JAR=/app/api.jar

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080 9999
ENTRYPOINT ["/docker-entrypoint.sh"]