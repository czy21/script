#!/bin/bash

exec java ${JAVA_OPTS} -jar ${JAR} --spring.config.additional-location=/app/conf/ --spring.profiles.active=${SPRING_PROFILES_ACTIVE} ${@}