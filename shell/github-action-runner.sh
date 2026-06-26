#!/bin/bash

# curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.335.1/actions-runner-linux-x64-2.335.1.tar.gz

for i in $(seq 1 3);do
  runner_name=openwrt-runner-$i
  mkdir -p $runner_name
  tar xzf actions-runner.tar.gz -C $runner_name
done