#!/bin/bash

set -e

cd /opt/jvm
rm -rf /opt/jvm/*
mkdir -p /opt/jvm/jdk11
git clone --branch jdk-11.0.11-ga https://gitee.com/czyhome/jdk11u.git jdk11
apt-get install -y openjdk-11-jdk build-essential zip unzip make autoconf libx11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev libcups2-dev libfontconfig1-dev libasound2-dev
cd jdk11
#bash configure --with-num-cores=4 --with-memory-size=8192 --disable-warnings-as-errors
bash configure
make images