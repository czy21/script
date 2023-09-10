#!/bin/bash
nginx && pulsar-manager --spring.config.location=${SPRING_CONFIGURATION_FILE} ${JAVA_ARGS}