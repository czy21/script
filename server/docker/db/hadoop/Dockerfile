FROM openjdk:8-jdk
ENV HADOOP_VERSION=3.2.3
ENV HADOOP_TGZ_URL=https://dlcdn.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH
COPY sources.list /etc/apt/
#COPY ___temp/hadoop-$HADOOP_VERSION.tar.gz $HADOOP_HOME/src.tgz
RUN mkdir -p $HADOOP_HOME $HADOOP_HOME/hdfs/name/ $HADOOP_HOME/hdfs/data/
RUN wget -nv -O $HADOOP_HOME/src.tgz $HADOOP_TGZ_URL;
RUN tar -xf $HADOOP_HOME/src.tgz --strip-components=1 -C $HADOOP_HOME && rm $HADOOP_HOME/src.tgz && chown -R root:root $HADOOP_HOME
RUN rm -rf $HADOOP_HOME/share/doc/;

ARG SSH_PUB='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com'
RUN apt-get update;
RUN apt-get install -y openssh-server net-tools vim git;
RUN sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
RUN echo 'UseDNS no \nPermitRootLogin yes \nPasswordAuthentication yes \nClientAliveInterval 30' >> /etc/ssh/sshd_config;
RUN cat /etc/ssh/sshd_config
RUN su root bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo ${SSH_PUB} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'
RUN su root bash -c 'cd;ssh-keygen -t rsa -f ~/.ssh/id_rsa; cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys'

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
EXPOSE 22 9870 9000
ENTRYPOINT ["/docker-entrypoint.sh"]
