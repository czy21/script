FROM alpine:3.11
ARG FRP_VERSION=0.33.0
WORKDIR /root/

RUN mkdir -p /usr/local/frp/conf/
RUN apk add --no-cache wget
RUN wget https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_amd64.tar.gz -O - | tar -zxvf - --strip-components 1 -C /usr/local/frp/

VOLUME /usr/local/frp/conf/
ENTRYPOINT /usr/local/frp/frps -c /usr/local/frp/conf/frps.ini