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
    for r in `find /etc/yum.repos.d/ -maxdepth 1 -name "rocky*.repo"`;do
      r_bak="${r}.bak"
      [ ! -f "${r_bak}" ] && cp -rv ${r} ${r_bak}
      sed -e 's|^mirrorlist=|#\0|g' -e "s|^#baseurl=http://dl.rockylinux.org/\$contentdir|baseurl=http://{{ param_mirror_yum }}/rocky|g" ${r_bak} | tee ${r} > /dev/null
    done
fi

if [ "fedora" = "${os_distribution}" ]; then
    for r in `find /etc/yum.repos.d/ -maxdepth 1 ! -name "fedora-cisco*.repo" -name "fedora*.repo"`;do
      r_bak="${r}.bak"
      [ ! -f "${r_bak}" ] && cp -rv ${r} ${r_bak}
      sed -e "s|^metalink=|#\0|g" \
          -e "s|#baseurl=http://download.example/pub/fedora/linux|baseurl=http://{{ param_mirror_yum }}/fedora|" \
          -e "s|/SRPMS/|/source/tree/|" ${r_bak} | tee ${r} > /dev/null
    done
fi

if [ "ubuntu" = "${os_distribution}" ]; then
  sources_file=/etc/apt/sources.list
  if [ "24" = "${os_major_version}" ];then
    sources_file=/etc/apt/sources.list.d/ubuntu.sources
  fi
  [ ! -f "${sources_file}.bak" ] && cp -rv ${sources_file} ${sources_file}.bak
  sed "s,\(http\|https\)://.*.ubuntu.com,http://{{ param_mirror_apt }}," ${sources_file}.bak | tee ${sources_file} > /dev/null
fi