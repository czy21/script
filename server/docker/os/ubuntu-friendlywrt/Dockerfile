FROM {{ param_registry_url }}/{{ param_registry_dir }}/ubuntu-openwrt-base

RUN wget -O - https://raw.githubusercontent.com/friendlyarm/build-env-on-ubuntu-bionic/master/install.sh | bash
RUN apt-get clean
RUN ln -sf /usr/bin/python2 /usr/bin/python

RUN su {{ param_user_ops }} bash -c 'git config --global user.email "{{ param_user_ops }}@localhost" && git config --global user.name "{{ param_user_ops }}"'