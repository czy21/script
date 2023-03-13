FROM jenkins/jenkins:2.394-jdk11
USER root
RUN apt update && apt install sudo -y
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins
USER jenkins