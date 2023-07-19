FROM jenkins/jenkins:2.414-jdk11
USER root
RUN apt update && apt install sudo -y
RUN curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins
USER jenkins