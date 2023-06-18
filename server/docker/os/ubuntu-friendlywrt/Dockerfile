FROM registry.czy21-internal.com/library/ubuntu-openwrt-base

RUN wget -O - https://raw.githubusercontent.com/friendlyarm/build-env-on-ubuntu-bionic/master/install.sh | bash
RUN apt-get clean

RUN su {{ param_user_ops }} bash -c 'git config --global user.email "{{ param_user_ops }}@localhost" && git config --global user.name "{{ param_user_ops }}"'