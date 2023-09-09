#!/bin/bash

java -Dloader.path=lib -Dspring.profiles.active=release ${JAVA_OPTS} -jar chat2db-server-start.jar