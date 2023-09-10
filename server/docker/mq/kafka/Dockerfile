FROM openjdk:11-jdk

ENV KAFKA_VERSION=2.13-3.4.1
ENV KAFKA_TGZ_URL=https://downloads.apache.org/kafka/3.4.1/kafka_${KAFKA_VERSION}.tgz
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$KAFKA_HOME/bin:$PATH

RUN mkdir -p $KAFKA_HOME
#COPY ___temp/kafka_${KAFKA_VERSION}.tgz $KAFKA_HOME/src.tgz
RUN wget -nv -O $KAFKA_HOME/src.tgz $KAFKA_TGZ_URL;
RUN tar -xf $KAFKA_HOME/src.tgz --strip-components=1 -C $KAFKA_HOME && rm $KAFKA_HOME/src.tgz && chown -R root:root $KAFKA_HOME
RUN rm -rf $KAFKA_HOME/site-docs

WORKDIR $KAFKA_HOME

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/logs"]
ENTRYPOINT ["/docker-entrypoint.sh"]