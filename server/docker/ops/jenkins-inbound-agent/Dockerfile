FROM busybox:1.35.0 as builder
USER root

RUN wget -O - https://get.helm.sh/helm-v{{ param_helm_version }}-linux-amd64.tar.gz | tar -zxf - --strip-components 1 -C /root linux-amd64/helm

FROM jenkins/inbound-agent:3261.v9c670a_4748a_9-2-alpine-jdk17
USER root

COPY --from=builder /root/helm /usr/local/bin/helm

RUN chown root:root /usr/local/bin/helm && chmod +x /usr/local/bin/helm
RUN ln -sf /usr/local/bin/helm /usr/bin/helm