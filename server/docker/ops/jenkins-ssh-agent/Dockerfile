FROM jenkins/ssh-agent:4.8.0-jdk11
USER root
RUN apt update && apt install git sudo -y
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins