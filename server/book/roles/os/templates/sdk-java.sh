#!/bin/bash
set -e

sudo mkdir -p /usr/local/java
versions="24.0.2 21.0.2 17.0.9"
for t in ${versions};do
  wget -O - https://github.com/graalvm/graalvm-ce-builds/releases/download/jdk-${t}/graalvm-community-jdk-${t}_linux-x64_bin.tar.gz | sudo tar -zxf - -C /usr/local/java
done