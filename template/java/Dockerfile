FROM openjdk:11.0.10-jre
WORKDIR /home/${{{param_project_name}}}_${{{param_api_module_name}}}
VOLUME ["/home/${{{param_project_name}}}_${{{param_api_module_name}}}/log","/home/${{{param_project_name}}}_${{{param_api_module_name}}}/config/"]

COPY ./api.jar /home/${{{param_project_name}}}_${{{param_api_module_name}}}/

RUN wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.15.0/jmx_prometheus_javaagent-0.15.0.jar

RUN ls -al /home/${{{param_project_name}}}_${{{param_api_module_name}}}/

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
EXPOSE ${{{param_api_container_port}}}
ENTRYPOINT ["java",\
"-javaagent:/home/${{{param_project_name}}}_${{{param_api_module_name}}}/jmx_prometheus_javaagent-0.15.0.jar=${{{param_api_jmx_port}}}:/home/${{{param_project_name}}}_${{{param_api_module_name}}}/config/${{{param_api_jmv_config_name}}}",\
"-jar",\
"/home/${{{param_project_name}}}_${{{param_api_module_name}}}/api.jar",\
"--spring.config.location=classpath:/,file:/home/${{{param_project_name}}}_${{{param_api_module_name}}}/config/"]