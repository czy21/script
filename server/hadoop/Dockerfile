FROM centos:7.6.1810
MAINTAINER bruce
ENV container docker
WORKDIR /root/
COPY ./___temp/ .
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
RUN echo "root:root" | chpasswd
RUN rpm -ivh jdk-8u241-linux-x64.rpm
RUN tar -zxvf hadoop-3.2.1.tar.gz -C /usr/local/
ENV JAVA_HOME=/usr/java/jdk1.8.0_241-amd64 HADOOP_HOME=/usr/local/hadoop-3.2.1
ENV PATH $JAVA_HOME/bin:$HADOOP_HOME/bin:$PATH
EXPOSE 22
VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init","/usr/sbin/sshd","-D"]