#!/bin/bash
set -e

os_distribution="{{ ansible_distribution | lower}}"
os_major_version="{{ ansible_distribution_major_version | lower }}"
os_product_name="{{ ansible_product_name }}"

if [ "centos" == "${os_distribution}" ]; then
    case ${os_major_version} in
        "9")
            if [ ! -f "/etc/yum.repos.d/centos.repo.bak" ];then
              cp /etc/yum.repos.d/centos.repo /etc/yum.repos.d/centos.repo.bak
            fi
            if [ ! -f "/etc/yum.repos.d/centos-addons.repo.bak" ];then
              cp /etc/yum.repos.d/centos-addons.repo /etc/yum.repos.d/centos-addons.repo.bak
            fi
            cp -r {{ param_remote_role_path }}/*.repo /etc/yum.repos.d/
            ;;
        *)
          echo "nothing"
    esac
fi

if [ "rocky" == "${os_distribution}" ]; then
    case ${os_major_version} in
        "9")
            for r in `find /etc/yum.repos.d/*.repo -maxdepth 1 -name "rocky*.repo"`;do
              r_bak="${r}.bak"
              if [ ! -f "${r_bak}" ];then
                cp ${r} ${r_bak}
              fi
              sed -e 's|^mirrorlist=|#mirrorlist=|g' -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=http://{{ param_mirror_yum }}/rocky|g' ${r_bak} > ${r}
            done
            ;;
        *)
          echo "nothing"
    esac
fi

if [ "ubuntu" == "${os_distribution}" ]; then
  if [ ! -f "/etc/apt/sources.list.bak" ];then
    cp /etc/apt/sources.list /etc/apt/sources.list.bak
  fi
  sed "s,\(http\|https\)://.*.ubuntu.com,http://{{ param_mirror_apt }},g" /etc/apt/sources.list.bak > /etc/apt/sources.list
fi

echo -n "
UseDNS no
PermitRootLogin yes
PasswordAuthentication no
ClientAliveInterval 30
" > /etc/ssh/sshd_config.d/99-custom.conf