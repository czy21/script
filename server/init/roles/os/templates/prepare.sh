#!/bin/bash
set -e

os_distribution="{{ ansible_distribution | lower}}"
os_major_version="{{ ansible_distribution_major_version | lower }}"

if [ "centos" == ${os_distribution} ]; then
    case ${os_major_version} in
        "9")
            if [ -f "/etc/yum.repos.d/centos.repo" ];then
              mv /etc/yum.repos.d/centos.repo /etc/yum.repos.d/centos.repo.bak
            fi
            if [ -f "/etc/yum.repos.d/addons.repo" ];then
              mv /etc/yum.repos.d/centos-addons.repo /etc/yum.repos.d/centos-addons.repo.bak
            fi
            repo_sections=("BaseOS" "AppStream" "CRB" "HighAvailability" "NFV" "RT")
            repo_section_types=("Debug" "Source")
            repo_private="/etc/yum.repos.d/centos-private.repo"
            echo -n "" > ${repo_private}
            for s in ${repo_sections[@]}; do
                sl=$(echo "$s" | tr "[:upper:]" "[:lower:]")
                s_baseurl="http://{{ param_mirror_yum }}/centos-stream/\$stream/$s/\$basearch/os/"
                s_enabled="0"
                if [ "BaseOS" == "${s}" ] || [ "AppStream" == "${s}" ] ; then
                  s_enabled="1"
                fi
                echo -n "
                  [${sl}]
                  name=CentOS Stream \$releasever - ${s}
                  baseurl=${s_baseurl}
                  gpgcheck=1
                  enabled=${s_enabled}
                  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial
                " | sed -r 's|^[ \t]*||g' >> ${repo_private}
                for t in ${repo_section_types[@]}; do
                  tl=$(echo "$t" | tr "[:upper:]" "[:lower:]")
                  tl=${sl}"-"${tl}
                  t_baseurl="http://{{ param_mirror_yum }}/centos-stream/\$stream/$s"
                  if [ "Debug" == ${t} ];then
                    tl+="info"
                    t_baseurl+="/\$basearch/debug/"
                  elif [ "Source" == ${t} ]; then
                      t_baseurl+="/source/"
                  fi
                echo -n "
                  [${tl}]
                  name=CentOS Stream \$releasever - ${s} - ${t}
                  baseurl=${t_baseurl}
                  gpgcheck=1
                  enabled=0
                  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial
                " | sed -r 's|^[ \t]*||g' >> ${repo_private}
                done
            done
            ;;
        *)
          sed -i.bak \
          -e "s,^mirrorlist=,#mirrorlist=,g" \
          -e "s,^#baseurl=,baseurl=,g" \
          -e "s,^baseurl=http://mirror.centos.org,baseurl=http://{{ param_mirror_yum }},g" /etc/yum.repos.d/CentOS-*.repo
    esac
fi

