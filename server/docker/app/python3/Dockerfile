FROM python:3.10-slim
ENV TZ=Asia/Shanghai
COPY sources.list /etc/apt/

RUN apt-get update && apt-get install gcc -y && apt-get clean