From openjdk:11.0.4-jdk-slim
VOLUME /home/erp
ARG jar
COPY ${jar} /home/erp/api.jar
ENTRYPOINT ["java","-jar","/home/erp/api.jar"]