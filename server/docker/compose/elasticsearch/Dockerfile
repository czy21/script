FROM openjdk:11-jdk
ARG SSH_PUB='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com'
RUN apt-get update;
RUN apt-get install -y openssh-server net-tools vim git sudo;
RUN sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
RUN echo 'UseDNS no \nPermitRootLogin yes \nPasswordAuthentication yes \nClientAliveInterval 30' >> /etc/ssh/sshd_config;

RUN useradd -m elastic -d /home/elastic -s /bin/bash;passwd -d elastic;
RUN groupadd wheel
RUN echo '%wheel ALL=(ALL:ALL)  NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG wheel elastic
RUN su root bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo ${SSH_PUB} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'
RUN su elastic bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo ${SSH_PUB} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'

# elasticsearch
ENV ES_TGZ_URL=https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.14.0-linux-x86_64.tar.gz
ENV ES_HOME=/opt/elasticsearch
ENV PATH=$ES_HOME/bin:$PATH
RUN set -ex; \
    mkdir -p $ES_HOME; \
    wget -nv -O $ES_HOME/src.tgz $ES_TGZ_URL; \
    tar -xf $ES_HOME/src.tgz --strip-components=1 -C $ES_HOME; \
    rm $ES_HOME/src.tgz; \
    chown -R elastic:elastic $ES_HOME;

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
