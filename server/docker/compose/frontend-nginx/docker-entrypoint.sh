#!/bin/bash


#RUN wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.15.0/jmx_prometheus_javaagent-0.15.0.jar

java -jar ${JAR} --spring.config.location=file:${CONFIG_DIR}