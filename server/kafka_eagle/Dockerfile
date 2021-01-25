FROM java:11-alpine

ARG KAFKA_EAGLE_VERSION=2.0.3
WORKDIR /root/
COPY ./___temp/ .

RUN tar zxf kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz --strip-components=1 -C /usr/local/kafka_eagle/

VOLUME /usr/local/kafka_eagle/conf/
ENTRYPOINT ["top"]