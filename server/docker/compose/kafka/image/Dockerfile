FROM openjdk:11-jre

RUN apt-get update;

ENV KAFKA_TGZ_URL=https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$KAFKA_HOME/bin:$PATH

RUN set -ex; \
    wget -nv -O $KAFKA_HOME/src.tgz "$KAFKA_TGZ_URL"; \
    tar -xf $KAFKA_HOME/src.tgz --strip-components=1 -C $KAFKA_HOME; \
    rm $KAFKA_HOME/src.tgz;

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]