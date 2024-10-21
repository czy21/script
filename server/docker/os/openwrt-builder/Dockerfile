FROM ubuntu:22.04

RUN apt-get update
# basic pkg
RUN apt install -y wget vim git bash-completion make gcc sudo curl

RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN useradd -d /home/buildbot -l -m -s /bin/bash buildbot && usermod -aG sudo buildbot

# https://openwrt.org/docs/guide-developer/toolchain/install-buildsystem
# official pkg
RUN apt install -y build-essential clang flex bison g++ gawk gcc-multilib g++-multilib gettext git libncurses-dev libssl-dev python3-distutils python3-setuptools rsync swig unzip zlib1g-dev file wget

# addition pkg
RUN apt install -y python3-dev python3-pyelftools qemu-utils libelf-dev

# tool
RUN curl https://dl.min.io/client/mc/release/linux-amd64/mc -o /usr/local/bin/mc
RUN chmod +x /usr/local/bin/mc && ln -sf /usr/local/bin/mc /usr/bin/mc

RUN apt-get clean

USER buildbot
WORKDIR /data