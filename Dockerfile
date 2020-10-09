FROM python:3

WORKDIR /usr/src/app
ARG REQ_TXT
COPY ${REQ_TXT} ./
RUN pip install --no-cache-dir -r requirements.txt