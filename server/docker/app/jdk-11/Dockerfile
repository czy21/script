FROM openjdk:11.0.10-jre
WORKDIR /home/app

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ENV JAR=/home/app/api.jar

RUN wget -nv -O /home/app/jmx-agent.jar https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.16.1/jmx_prometheus_javaagent-0.16.1.jar;

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/home/app/default","/home/app/config/","/home/app/data/"]
EXPOSE 8080
EXPOSE 8088
ENTRYPOINT ["/docker-entrypoint.sh"]