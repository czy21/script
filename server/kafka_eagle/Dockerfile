FROM java:8-alpine

ARG KAFKA_EAGLE_VERSION=2.0.3
WORKDIR /root/
COPY ./___temp/ .

RUN tar zxf kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz -C /usr/local/

ENV KE_HOME=/usr/local/kafka-eagle-web-${KAFKA_EAGLE_VERSION}
ENV PATH $KE_HOME/bin:$PATH

VOLUME /usr/local/kafka-eagle-web-${KAFKA_EAGLE_VERSION}/conf/
VOLUME /usr/local/kafka-eagle-web-${KAFKA_EAGLE_VERSION}/logs/

EXPOSE 8048
ENTRYPOINT sh $KE_HOME/bin/ke.sh start