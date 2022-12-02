#!/bin/bash
set -e

os_distribution="{{ ansible_distribution | lower}}"
os_major_version="{{ ansible_distribution_major_version | lower }}"

if [ "centos" == "${os_distribution}" ]; then
    case ${os_major_version} in
        "9")
            if [ -f "/etc/yum.repos.d/centos.repo" ];then
              mv /etc/yum.repos.d/centos.repo /etc/yum.repos.d/centos.repo.bak
            fi
            if [ -f "/etc/yum.repos.d/centos-addons.repo" ];then
              mv /etc/yum.repos.d/centos-addons.repo /etc/yum.repos.d/centos-addons.repo.bak
            fi
            repo_sections=("BaseOS" "AppStream" "CRB" "HighAvailability" "NFV" "RT" "ResilientStorage")
            repo_section_types=("Debug" "Source")
            repo_proxy=""
            for s in ${repo_sections[*]}; do
                s_baseurl="http://{{ param_mirror_yum }}/centos-stream/\$stream/$s/\$basearch/os/"
                s_enabled="0"
                if [ "BaseOS" == "${s}" ] || [ "AppStream" == "${s}" ] ; then
                  s_enabled="1"
                fi
                sl=$(echo "$s" | tr "[:upper:]" "[:lower:]")
                repo_proxy_text+="
                  [${sl}]
                  name=CentOS Stream \$releasever - ${s}
                  baseurl=${s_baseurl}
                  gpgcheck=1
                  enabled=${s_enabled}
                  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial
                "
                for t in ${repo_section_types[*]}; do
                  tl=$(echo "$t" | tr "[:upper:]" "[:lower:]")
                  tl=${sl}"-"${tl}
                  t_baseurl="http://{{ param_mirror_yum }}/centos-stream/\$stream/$s"
                  if [ "Debug" == ${t} ];then
                    tl+="info"
                    t_baseurl+="/\$basearch/debug/"
                  elif [ "Source" == ${t} ]; then
                      t_baseurl+="/source/"
                  fi
                  repo_proxy_text+="
                    [${tl}]
                    name=CentOS Stream \$releasever - ${s} - ${t}
                    baseurl=${t_baseurl}
                    gpgcheck=1
                    enabled=0
                    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial
                  "
                done
            done
                repo_proxy_text+="
                  [extras-common]
                  name=CentOS Stream \$releasever - Extras packages
                  metalink=https://mirrors.centos.org/metalink?repo=centos-extras-sig-extras-common-\$stream&arch=\$basearch&protocol=https,http
                  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-Extras-SHA512
                  gpgcheck=1
                  repo_gpgcheck=0
                  metadata_expire=6h
                  countme=1
                  enabled=1

                  [extras-common-source]
                  name=CentOS Stream \$releasever - Extras packages - Source
                  metalink=https://mirrors.centos.org/metalink?repo=centos-extras-sig-extras-common-source-\$stream&arch=source&protocol=https,http
                  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-Extras-SHA512
                  gpgcheck=1
                  repo_gpgcheck=0
                  metadata_expire=6h
                  enabled=0
                "
                echo "$repo_proxy_text" | sed -r 's|^[ \t]*||g' > "/etc/yum.repos.d/centos-proxy.repo"
            ;;
        *)
          sed -i.bak \
          -e "s,^mirrorlist=,#mirrorlist=,g" \
          -e "s,^#baseurl=,baseurl=,g" \
          -e "s,^baseurl=http://mirror.centos.org,baseurl=http://{{ param_mirror_yum }},g" /etc/yum.repos.d/CentOS-*.repo
    esac
fi

if [ "ubuntu" == "${os_distribution}" ]; then
  sed -i.bak "s,\(http\|https\)://.*.ubuntu.com,http://{{ param_mirror_apt }},g" /etc/apt/sources.list
fi

echo -n "
UseDNS no
PermitRootLogin yes
PasswordAuthentication no
ClientAliveInterval 30
" > /etc/ssh/sshd_config.d/99-custom.conf