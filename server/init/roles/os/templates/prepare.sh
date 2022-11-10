#!/bin/bash
set -e

os_distribution="{{ ansible_distribution | lower}}"
os_major_version="{{ ansible_distribution_major_version | lower }}"

if [ "centos" == ${os_distribution} ]; then
    case ${os_major_version} in
        "9")
            echo "这是9哦"
            ;;
        *)
          sed -i.bak \
          -e "s,^mirrorlist=,#mirrorlist=,g" \
          -e "s,^#baseurl=,baseurl=,g" \
          -e "s,^baseurl=http://mirror.centos.org,baseurl=http://{{ param_mirror_yum }},g" /etc/yum.repos.d/CentOS-*.repo
    esac
fi

