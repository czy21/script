FROM centos:8.3.2011

RUN sed -i.bak -e "s,^mirrorlist=,#mirrorlist=,g" -e "s,^#baseurl=,baseurl=,g" -e "s,^baseurl=http://mirror.centos.org/\$contentdir,baseurl=http://{{ param_mirror_yum_centos_vault }},g" /etc/yum.repos.d/CentOS-*.repo
RUN yum clean all && yum makecache