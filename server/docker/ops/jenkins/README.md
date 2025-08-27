## Mirror
```text
https://mirrors.huaweicloud.com/jenkins/update-center.json
```
## Ignore sign check
```shell
-Dhudson.model.DownloadService.noSignatureCheck=true
```
## Manual update plugin
```shell
cd /var/jenkins_home/plugin
pkgs="cloudbees-folder"
for p in $pkgs;do
  curl -sSL -o $p.jpi https://updates.jenkins.io/latest/$p.hpi
done
```