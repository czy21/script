#!/bin/bash

curl -fsSL https://archives.jenkins.io/updates/update-center.json | sed -e 's|connectionCheckUrl|connectionCheckUrlBak|' -e 's|https://updates.jenkins.io|https://{{ param_mirror_raw }}/jenkins|g' > {{ param_docker_data }}/nginx/static/jenkins-update-center.json
curl -u {{ param_manage_username }}:{{ param_manage_password}} --upload-file {{ param_docker_data }}/nginx/static/jenkins-update-center.json https://{{ param_mirror_host }}/raw-hosted/jenkins/update-center.json

updates_htmls=$(curl -s https://archives.jenkins.io/updates/updates/ | grep -o '<a href="[^"]*' | grep -o '[^"]*.html$' | grep -v '/$' | sort)

for t in ${updates_htmls};do
  echo ${t}
  content_source=$(curl -fsSL https://archives.jenkins.io/updates/updates/$t)
  content_target="${content_source}"
  case "$t" in
    "hudson.plugins.gradle.GradleInstaller.json.html")
      content_target=$(echo "$content_target" | sed -e 's|services.gradle.org/distributions|mirrors.nju.edu.cn/gradle|g')
      ;;
    "io.jenkins.plugins.dotnet.data.Downloads.json.html")
      content_target=$(echo "$content_target" | sed -e 's|builds.dotnet.microsoft.com|{{ param_mirror_host }}/raw-proxy/\0|g')
      ;;
    "io.jenkins.plugins.adoptopenjdk.AdoptOpenJDKInstaller.json.html")
      content_target=$(/root/.python3/bin/python3 /root/script/jenkins-adoptium.py)
      ;;
    *)
      ;;
  esac
  if [ "${content_source}" != "${content_target}" ];then
    echo "${content_source}" | curl -u {{ param_manage_username }}:{{ param_manage_password}} -T - https://{{ param_mirror_host }}/raw-hosted/jenkins/updates/$t.original
  fi
  echo "${content_target}" | curl -u {{ param_manage_username }}:{{ param_manage_password}} -T - https://{{ param_mirror_host }}/raw-hosted/jenkins/updates/$t
done