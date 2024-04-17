FROM ghcr.io/graalvm/graalvm-community:17.0.9-ol7-20231024

LABEL org.opencontainers.image.url='https://github.com/czy21/container'
LABEL org.opencontainers.image.source='https://github.com/czy21/container/tree/main/graalvm-jdk-17'
LABEL org.opencontainers.image.title='based on graalvm/graalvm-community:17.0.9'
LABEL org.opencontainers.image.authors='a805899926@gmail.com>'

WORKDIR /app
ENV JAR=/app/api.jar

RUN mkdir conf

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/app/data/","/app/log"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]