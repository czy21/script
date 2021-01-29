FROM java:8-alpine

ARG KAFKA_EAGLE_VERSION=2.0.3
WORKDIR /root/
COPY ./___temp/ .

RUN tar -zxf kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz -C /usr/local/ \
 && mv /usr/local/kafka-eagle-web-${KAFKA_EAGLE_VERSION} /usr/local/kafka_eagle/ \
 && rm -rf kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz

ENV KE_HOME=/usr/local/kafka_eagle
ENV PATH $KE_HOME/bin:$PATH

RUN apk add --no-cache bash && mkdir -p /tmp/shell/
COPY run.sh /tmp/shell/

RUN chmod a+x /tmp/shell/*.sh \
 && mv /tmp/shell/run.sh /usr/bin \
 && sync \
 && rm -rf /tmp/shell/

EXPOSE 8048
VOLUME ["$KE_HOME/logs/","$KE_HOME/conf/"]
ENTRYPOINT ["run.sh"]