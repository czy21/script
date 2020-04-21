FROM centos:7.6.1810
ARG HADOOP_VERSION=3.2.1
ARG JDK_VERSION=1.8
WORKDIR /root/
COPY ./___temp/ .
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
RUN sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
RUN yum clean all;yum makecache;
RUN yum -y install wget vim openssh-server openssh-clients;
RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
RUN ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN mkdir .ssh/ && chmod 700 .ssh/
RUN ssh-keygen -t rsa -f .ssh/id_rsa
RUN cat .ssh/id_rsa.pub > .ssh/authorized_keys
RUN echo "root:root" | chpasswd
RUN mkdir -p /usr/local/java/jdk${JDK_VERSION} && tar -zxf jdk-${JDK_VERSION}.tar.gz --strip-components 1 -C /usr/local/java/jdk${JDK_VERSION}
RUN mkdir -p /usr/local/hadoop/ && tar -zxf hadoop-${HADOOP_VERSION}.tar.gz --strip-components 1 -C /usr/local/hadoop/
ENV JAVA_HOME=/usr/local/java/jdk${JDK_VERSION} HADOOP_HOME=/usr/local/hadoop
ENV PATH $JAVA_HOME/bin:$HADOOP_HOME/bin:$PATH
RUN rm -rf jdk-${JDK_VERSION}.tar.gz hadoop-${HADOOP_VERSION}.tar.gz
# hadoop config start
COPY ./etc/* /usr/local/hadoop/etc/hadoop/
RUN sed -i -r "s/^\s*# (export JAVA_HOME=)/\1\/usr\/local\/java\/jdk${JDK_VERSION}/" /usr/local/hadoop/etc/hadoop/hadoop-env.sh
RUN sed -i "N;16 a HDFS_DATANODE_USER=root\nHDFS_DATANODE_SECURE_USER=hdfs\nHDFS_NAMENODE_USER=root\nHDFS_SECONDARYNAMENODE_USER=root\n" /usr/local/hadoop/sbin/start-dfs.sh
RUN sed -i "N;16 a HDFS_DATANODE_USER=root\nHDFS_DATANODE_SECURE_USER=hdfs\nHDFS_NAMENODE_USER=root\nHDFS_SECONDARYNAMENODE_USER=root\n" /usr/local/hadoop/sbin/stop-dfs.sh
RUN sed -i "N;16 a YARN_RESOURCEMANAGER_USER=root\nHADOOP_SECURE_DN_USER=yarn\nYARN_NODEMANAGER_USER=root" /usr/local/hadoop/sbin/start-yarn.sh
RUN sed -i "N;16 a YARN_RESOURCEMANAGER_USER=root\nHADOOP_SECURE_DN_USER=yarn\nYARN_NODEMANAGER_USER=root" /usr/local/hadoop/sbin/stop-yarn.sh
RUN mkdir /usr/local/hadoop/tmp && mkdir /usr/local/hadoop/hdfs && mkdir /usr/local/hadoop/hdfs/data && mkdir /usr/local/hadoop/hdfs/name
# hadoop config end
EXPOSE 22
VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init","/usr/sbin/sshd","-D"]