FROM jenkins/ssh-agent:5.1.0-jdk17
USER root
RUN apt update && apt install git sudo -y
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins