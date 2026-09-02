#!/bin/bash
set -e

sudo install -m 0755 -d /usr/local/java

for t in {{ param_sdk_java_versions | replace(',', ' ') }};do
  wget -nv -O - https://github.com/graalvm/graalvm-ce-builds/releases/download/jdk-${t}/graalvm-community-jdk-${t}_linux-x64_bin.tar.gz | sudo tar -zxf - -C /usr/local/java
done