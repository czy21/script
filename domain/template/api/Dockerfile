From openjdk:11-jdk-alpine
VOLUME /home/erp
ARG jar
COPY ${jar} /home/erp/api.jar
ENTRYPOINT ["java","-jar","/home/erp/api.jar"]