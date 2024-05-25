FROM busybox:1.35.0 as builder
USER root

RUN wget -O - https://get.helm.sh/helm-v3.13.3-linux-amd64.tar.gz | tar -zxf - --strip-components 1 -C /root linux-amd64/helm

FROM jenkins/inbound-agent:3248.v65ecb_254c298-3-alpine-jdk17
USER root

COPY --from=builder /root/helm /usr/local/bin/helm

RUN chown root:root /usr/local/bin/helm && chmod +x /usr/local/bin/helm
RUN ln -sf /usr/local/bin/helm /usr/bin/helm