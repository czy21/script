FROM ghcr.io/graalvm/jdk-community:23.0.1

WORKDIR /app
ENV JAR=/app/api.jar

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080 9999
ENTRYPOINT ["/docker-entrypoint.sh"]