FROM openjdk:11-jre-slim
VOLUME ["/home/${{{param_project_name}}}/log"]

COPY ./api.jar /home/${{{param_project_name}}}/
COPY ./resources/ /home/${{{param_project_name}}}/resources/
RUN ls -al /home/${{{param_project_name}}}/

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
EXPOSE ${{{param_api_container_port}}}
ENTRYPOINT ["java","-jar","/home/${{{param_project_name}}}/api.jar","--spring.config.location=/home/${{{param_project_name}}}/resources/"]