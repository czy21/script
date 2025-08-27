#!/bin/bash

curl -fsSL https://updates.jenkins.io/update-center.json | sed -e 's|connectionCheckUrl|connectionCheckUrlBak|' -e 's|https://updates.jenkins.io|https://{{ param_mirror_raw}}/jenkins|g' > {{ param_docker_data }}/nginx/static/jenkins-update-center.json