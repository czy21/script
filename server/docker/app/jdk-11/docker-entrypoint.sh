#!/bin/bash
JMX_ARGS=-Dcom.sun.management.jmxremote.port=9999 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false
exec java ${JMX_ARGS} ${JAVA_OPTS} -jar ${JAR} --spring.config.additional-location=/app/conf/ ${@}