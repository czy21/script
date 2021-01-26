FROM alpine:3.10

ARG KAFKA_EAGLE_VERSION=2.0.3
ARG JDK_VERSION=11.0.9
WORKDIR /root/
COPY ./___temp/ .

RUN echo -e "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.4/main\n\
https://mirror.tuna.tsinghua.edu.cn/alpine/v3.4/community" > /etc/apk/repositories

RUN apk --update add curl bash openjdk8 && rm -rf /var/cache/apk/*
RUN mkdir -p /usr/local/kafka_eagle/ && tar zxf kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz --strip-components 1 -C /usr/local/kafka_eagle/

RUN rm -rf jdk-${JDK_VERSION}_linux-x64_bin.tar.gz kafka-eagle-web-${KAFKA_EAGLE_VERSION}-bin.tar.gz

ENV JAVA_HOME=/usr/lib/jvm/default-jvm KE_HOME=/usr/local/kafka_eagle
ENV PATH $JAVA_HOME/bin:$KE_HOME/bin:$PATH

VOLUME $KE_HOME/conf/
VOLUME $KE_HOME/logs/

EXPOSE 8048
ENTRYPOINT sh $KE_HOME/bin/ke.sh start