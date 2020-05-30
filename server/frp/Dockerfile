FROM alpine:3.11
ARG FRP_VERSION=0.32.0
WORKDIR /root/
COPY ./___temp/ .

RUN mkdir -p /usr/local/frp/conf/
RUN tar -zxvf frp_${FRP_VERSION}_linux_amd64.tar.gz --strip-components 1 -C /usr/local/frp/

VOLUME /usr/local/frp/conf/
ENTRYPOINT /usr/local/frp/frps -c /usr/local/frp/conf/frps.ini