#!/bin/bash
set -e

os_distribution="{{ param_ansible_distribution }}"
os_major_version="{{ param_ansible_distribution_major_version }}"
os_product_name="{{ param_ansible_product_name }}"

if [ "centos" = "${os_distribution}" ]; then
    case ${os_major_version} in
        "9")
            for r in `find /etc/yum.repos.d/ -maxdepth 1 -name "centos*.repo"`;do
              r_bak="${r}.bak"
              if [ ! -f "${r_bak}" ];then
                cp -rv ${r} ${r_bak}
              fi
            done
            cp -r {{ param_remote_role_path }}/*.repo /etc/yum.repos.d/
            ;;
        *)
          echo "nothing"
    esac
fi

if [ "rocky" = "${os_distribution}" ]; then
    case ${os_major_version} in
        "9")
            for r in `find /etc/yum.repos.d/ -maxdepth 1 -name "rocky*.repo"`;do
              r_bak="${r}.bak"
              if [ ! -f "${r_bak}" ];then
                cp -rv ${r} ${r_bak}
              fi
              sed -e 's|^mirrorlist=|#mirrorlist=|g' -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=http://{{ param_mirror_yum }}/rocky|g' ${r_bak} | tee ${r} > dev/null
            done
            ;;
        *)
          echo "nothing"
    esac
fi

if [ "ubuntu" = "${os_distribution}" ]; then
  if [ ! -f "/etc/apt/sources.list.bak" ];then
    cp -rv /etc/apt/sources.list /etc/apt/sources.list.bak
  fi
  sed "s,\(http\|https\)://.*.ubuntu.com,http://{{ param_mirror_apt }},g" /etc/apt/sources.list.bak | tee /etc/apt/sources.list > /dev/null
fi