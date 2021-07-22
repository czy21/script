#!/bin/bash

set -e
jvm_dir=/opt/jvm
jdk11_dir=${jvm_dir}/jdk11
if [ ! -d "${jdk11_dir}/build/" ];then
  rm -rf ${jdk11_dir} && mkdir -p ${jdk11_dir}
  git clone --branch jdk-11.0.11-ga https://gitee.com/czyhome/jdk11u.git ${jdk11_dir}
  apt-get install -y openjdk-11-jdk cmake gdb build-essential zip unzip make autoconf libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev libcups2-dev libfontconfig1-dev libasound2-dev
  cd ${jdk11_dir}
  echo echo -e "\033[32m start build"
  bash configure
  make images
fi