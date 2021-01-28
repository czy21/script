FROM java:8-alpine

ARG KAFKA_EAGLE_VERSION=2.0.3
WORKDIR /root/
COPY ./___temp/ .

RUN tar -zxf kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz -C /usr/local/ \
 && mv /usr/local/kafka-eagle-web-${KAFKA_EAGLE_VERSION} /usr/local/kafka_eagle/ \
 && rm -rf kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz \
 && chmod +x /usr/local/kafka_eagle/bin/ke.sh

ENV KE_HOME=/usr/local/kafka_eagle
ENV PATH $KE_HOME/bin:$PATH

VOLUME ["$KE_HOME/conf/","$KE_HOME/logs/"]

EXPOSE 8048

COPY run.sh ./
RUN chmod +x run.sh
ENTRYPOINT ["sh","run.sh"]