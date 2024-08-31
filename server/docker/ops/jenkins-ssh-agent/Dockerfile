FROM jenkins/ssh-agent:5.46.0-jdk17

USER root
RUN apt update && apt install git sudo curl -y
RUN curl -L "https://github.com/docker/compose/releases/download/v{{ param_compose_version }}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins