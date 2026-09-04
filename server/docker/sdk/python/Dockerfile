ARG BASE_IMAGE=python:3.10.18-slim

FROM $BASE_IMAGE

WORKDIR /app

RUN apt-get update && apt-get install gcc -y && apt-get clean

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]