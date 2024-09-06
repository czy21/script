#!/bin/bash
set -e

os_distribution="{{ param_ansible_distribution }}"
os_major_version="{{ param_ansible_distribution_major_version }}"

if [ "centos" = "${os_distribution}" ]; then
    case ${os_major_version} in
        "9")
            for r in `find /etc/yum.repos.d/ -maxdepth 1 -name "centos*.repo"`;do
              r_bak="${r}.bak"
              [ ! -f "${r_bak}" ] && cp -rv ${r} ${r_bak}
            done
            cp -r {{ param_remote_role_path }}/centos*.repo /etc/yum.repos.d/
            ;;
        *)
          echo "unknown os_major_version"
    esac
fi

if [ "rocky" = "${os_distribution}" ]; then
    case ${os_major_version} in
        "9")
            for r in `find /etc/yum.repos.d/ -maxdepth 1 -name "rocky*.repo"`;do
              r_bak="${r}.bak"
              [ ! -f "${r_bak}" ] && cp -rv ${r} ${r_bak}
              sed -e 's|^mirrorlist=|#mirrorlist=|g' -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=http://{{ param_mirror_yum }}/rocky|g' ${r_bak} | tee ${r} > /dev/null
            done
            ;;
        *)
          echo "unknown os_major_version"
    esac
fi

if [ "fedora" = "${os_distribution}" ]; then
    for r in `find /etc/yum.repos.d/ -maxdepth 1 -name "fedora*.repo"`;do
      r_bak="${r}.bak"
      [ ! -f "${r_bak}" ] && cp -rv ${r} ${r_bak}
    done
    cp -r {{ param_remote_role_path }}/fedora*.repo /etc/yum.repos.d/
fi

if [ "ubuntu" = "${os_distribution}" ]; then
  [ ! -f "/etc/apt/sources.list.bak" ] && cp -rv /etc/apt/sources.list /etc/apt/sources.list.bak
  sed "s,\(http\|https\)://.*.ubuntu.com,http://{{ param_mirror_apt }},g" /etc/apt/sources.list.bak | tee /etc/apt/sources.list > /dev/null
fi