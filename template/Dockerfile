FROM openjdk:11-jre-slim
WORKDIR /home/${{{param_project_name}}}
VOLUME ["/home/${{{param_project_name}}}/log"]

COPY ./api.jar /home/${{{param_project_name}}}/
COPY ./resources/ /home/${{{param_project_name}}}/resources/

RUN wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.15.0/jmx_prometheus_javaagent-0.15.0.jar

RUN ls -al /home/${{{param_project_name}}}/

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
EXPOSE ${{{param_api_container_port}}}
ENTRYPOINT ["java",
"-jar",
"/home/${{{param_project_name}}}/api.jar",
"--spring.config.location=/home/${{{param_project_name}}}/resources/"
]