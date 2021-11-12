FROM docker.elastic.co/logstash/logstash:7.14.0

USER root
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
USER 1000

ENV EXT_LIB=/usr/share/logstash/ext/lib/
RUN mkdir -p ${EXT_LIB}
COPY ___temp/lib/ ${EXT_LIB}