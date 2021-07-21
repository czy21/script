FROM ubuntu:18.04
WORKDIR /opt/jvm/
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
RUN apt-get update;
RUN apt-get install -y openssh-server sudo net-tools vim git openjdk-11-jdk;
RUN sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
RUN echo 'UseDNS no \nPermitRootLogin yes \nPasswordAuthentication yes \nClientAliveInterval 30' >> /etc/ssh/sshd_config;
RUN cat /etc/ssh/sshd_config
RUN useradd -m bruce -d /home/bruce -s /bin/bash;passwd -d bruce;
RUN groupadd wheel
RUN echo '%wheel ALL=(ALL:ALL)  NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG wheel bruce
RUN su bruce bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'

EXPOSE 22
ENTRYPOINT ["/docker-entrypoint.sh"]