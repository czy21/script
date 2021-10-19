FROM openjdk:11.0.10-jre
ENV WORKDIR=/home/app
WORKDIR ${WORKDIR}

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ENV JAVA_AGENT=${WORKDIR}/java-agent.jar
ENV JAR=${WORKDIR}/api.jar
ENV CONFIG_DIR=${WORKDIR}/config/
ENV DATA_DIR=${WORKDIR}/data/

RUN wget -nv -O ${JAVA_AGENT} https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.16.1/jmx_prometheus_javaagent-0.16.1.jar;

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["${CONFIG_DIR}","${DATA_DIR}"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]