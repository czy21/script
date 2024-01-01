FROM eclipse-temurin:17.0.9_9-jdk-jammy

ENV KAFKA_VERSION=2.13-3.6.1
ENV KAFKA_TGZ_URL=https://downloads.apache.org/kafka/3.6.1/kafka_${KAFKA_VERSION}.tgz
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$KAFKA_HOME/bin:$PATH

RUN mkdir -p $KAFKA_HOME
RUN wget -nv -O $KAFKA_HOME/src.tgz $KAFKA_TGZ_URL;
RUN tar -xf $KAFKA_HOME/src.tgz --strip-components=1 -C $KAFKA_HOME && rm $KAFKA_HOME/src.tgz && chown -R root:root $KAFKA_HOME
RUN rm -rf $KAFKA_HOME/site-docs

WORKDIR $KAFKA_HOME

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/logs"]
ENTRYPOINT ["/docker-entrypoint.sh"]