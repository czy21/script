FROM jenkins/ssh-agent:5.38.0-jdk11

LABEL org.opencontainers.image.url='https://github.com/czy21/container'
LABEL org.opencontainers.image.source='https://github.com/czy21/container/tree/main/jenkins-ssh-agent'
LABEL org.opencontainers.image.title='base on jenkins/ssh-agent:5.38.0-jdk11'
LABEL org.opencontainers.image.authors='a805899926@gmail.com>'

USER root
RUN apt update && apt install git sudo curl -y
RUN curl -L "https://github.com/docker/compose/releases/download/v{{ param_global_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins