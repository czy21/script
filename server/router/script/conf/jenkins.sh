#!/bin/bash

jenkins_static={{ param_docker_data }}/nginx/static/jenkins
jenkins_static_updates=${jenkins_static}/updates
mkdir -p ${jenkins_static_updates}

curl -fsSL https://updates.jenkins.io/update-center.json > ${jenkins_static}/update-center.json

sed -i \
  -e 's|connectionCheckUrl|connectionCheckUrlBak|' \
  -e 's|https://updates.jenkins.io|https://{{ param_mirror_raw }}/jenkins|g' \
  ${jenkins_static}/update-center.json

updates_files=$(curl -s https://updates.jenkins.io/updates/ | sed -n 's/.*href="\([^"]*\.json\)".*/\1/p')

echo '===== downloading ====='
for t in ${updates_files};do
  echo $t
  curl -fsSL "https://updates.jenkins.io/updates/$t" -o "${jenkins_static_updates}/$t"
done

echo '===== replacing ====='
for t in ${updates_files};do
  echo $t
  content_source=$(cat ${jenkins_static_updates}/$t)
  content_target="${content_source}"
  case "$t" in
    "hudson.plugins.nodejs.tools.NodeJSInstaller.json")
      content_target=$(echo "$content_target" | sed -e 's|https://nodejs.org/dist|https://mirrors.aliyun.com/nodejs-release|g')
      ;;
    "hudson.plugins.gradle.GradleInstaller.json")
      content_target=$(echo "$content_target" | sed -e 's|services.gradle.org/distributions|mirrors.nju.edu.cn/gradle|g')
      ;;
    "io.jenkins.plugins.dotnet.data.Downloads.json")
      content_target=$(echo "$content_target" | sed -e 's|builds.dotnet.microsoft.com|{{ param_mirror_host }}/raw-proxy/\0|g')
      ;;
    "io.jenkins.plugins.adoptopenjdk.AdoptOpenJDKInstaller.json")
      content_target=$(/root/.python3/bin/python3 /root/script/jenkins-adoptium.py --updates-dir ${jenkins_static_updates})
      ;;
    *)
      ;;
  esac
  if [ "${content_source}" != "${content_target}" ];then
    echo "${content_source}" > ${jenkins_static_updates}/$t.bak
  fi
  echo "${content_target}" > ${jenkins_static_updates}/$t
done

/root/.python3/bin/python3 /root/script/jenkins.py --updates-dir ${jenkins_static_updates}