FROM centos:8.3.2011

RUN sed -i -e "s,^mirrorlist=,#mirrorlist=,g" -e "s,^#baseurl=,baseurl=,g" -e "s,^baseurl=http://\(mirror\|vault\).centos.org,baseurl=http://{{ param_mirror_yum }},g" /etc/yum.repos.d/CentOS-*.repo

RUN cat /etc/yum.repos.d/CentOS-*.repo
RUN yum update -y