#!/bin/bash
set -e

jdk_from={{ param_remote_path }}/{{ param_jdk_from }}
jdk_root={{ param_jdk_root }}

mkdir -p $jdk_root

function install_jdk(){
  local sdk_name=$1
  local sdk_link=$2
  local sdk_file=$(basename $sdk_link)
  local sdk_home=${jdk_root}/$sdk_name
  if [ -f "${jdk_from}/${sdk_file}" ];then
    cp -rv ${jdk_from}/${sdk_file} ${sdk_home}.zip
  else 
    curl -fsSLo ${sdk_home}.zip $sdk_link
  fi
  mkdir -p ${sdk_home}
  unzip -qo ${sdk_home}.zip -d ${sdk_home}-temp && cp -rf ${sdk_home}-temp/*/* ${sdk_home}/ && rm -rf ${sdk_home}-temp ${sdk_home}.zip
}

{%- set install_jdks = ([param_jdk_home] + param_jdk_need) | unique %}
{%- set matched_jdks = param_jdk_versions | selectattr("name", "in", install_jdks) | list %}

{% for t in matched_jdks %}
install_jdk {{ t.name }} {{ t.link }}
{% endfor -%}