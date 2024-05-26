FROM jenkins/jenkins:2.459-jdk11

LABEL org.opencontainers.image.url='https://github.com/czy21/container'
LABEL org.opencontainers.image.source='https://github.com/czy21/container/tree/main/jenkins'
LABEL org.opencontainers.image.title='base on jenkins/jenkins:2.459-jdk11'
LABEL org.opencontainers.image.authors='a805899926@gmail.com>'

USER root
RUN apt update && apt install sudo -y
RUN curl -L "https://github.com/docker/compose/releases/download/v{{ param_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins
USER jenkins