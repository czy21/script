#!/bin/bash

set -e

cd /opt/jvm
rm -rf /opt/jvm/*
git clone https://gitee.com/czyhome/jdk11.git
apt-get install -y build-essential zip unzip make autoconf libx11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev libcups2-dev libfontconfig1-dev libasound2-dev
bash configure
make