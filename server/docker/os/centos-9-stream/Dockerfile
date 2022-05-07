FROM {{ param_registry_proxy_url | default("quay.io") }}/centos/centos:stream9

RUN sed -i.bak -e "s,^metalink=https://mirrors.centos.org,metalink=http://{{ param_mirror_yum }},g" /etc/yum.repos.d/centos-*.repo
RUN yum update -y