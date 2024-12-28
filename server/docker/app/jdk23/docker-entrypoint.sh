#!/bin/bash
exec java ${JAVA_OPTS} -jar ${JAR} --spring.config.additional-location=/app/conf/ ${@}