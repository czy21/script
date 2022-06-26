FROM {{ param_registry_proxy_url | default("quay.io") }}/centos/centos:stream8

RUN sed -i.bak -e "s,^mirrorlist=,#mirrorlist=,g" -e "s,^#baseurl=,baseurl=,g" -e "s,^baseurl=http://mirror.centos.org\contentdir,baseurl=http://{{ param_mirror_yum_centos }},g" /etc/yum.repos.d/CentOS-*.repo
RUN yum clean all && yum makecache

RUN yum -y install wget vim nfs-utils bash-completion git
RUN dnf -y install python39