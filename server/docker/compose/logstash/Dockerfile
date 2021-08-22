FROM docker.elastic.co/logstash/logstash:7.14.0

ENV EXT_LIB=/usr/share/logstash/ext/lib/

RUN mkdir -p ${EXT_LIB}
COPY ___temp/mysql-connector-java-8.0.25.jar ${EXT_LIB}