FROM {{ param_registry_proxy_url | default("quay.io") }}/centos/centos:stream8

RUN sed -i.bak -e "s,^mirrorlist=,#mirrorlist=,g" -e "s,^#baseurl=,baseurl=,g" -e "s,^baseurl=http://mirror.centos.org,baseurl=http://{{ param_mirror_yum }},g" /etc/yum.repos.d/CentOS-*.repo
RUN yum clean all && yum --refresh makecache

RUN yum -y install git