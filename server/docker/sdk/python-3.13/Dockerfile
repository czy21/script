FROM python:3.13.7-slim

WORKDIR /app

RUN apt-get update && apt-get install gcc -y && apt-get clean

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]