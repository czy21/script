FROM openjdk:11-jre

RUN apt-get update;

ENV KAFKA_TGZ_URL=https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$KAFKA_HOME/bin:$PATH

WORKDIR $KAFKA_HOME

RUN set -ex; \
    wget -nv -O kafka.tgz "$KAFKA_TGZ_URL"; \
    tar -xf kafka.tgz --strip-components=1; \
    rm kafka.tgz;

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]