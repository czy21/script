```shell
sudo hostnamectl set-hostname --static [hostname]
# ubuntu enable remote desktop
sudo apt install xrdp

# pull
rsync --archive --delete --progress --verbose rsync://<username>@<host>:<remote_path> <local_path>
```
## ssh
```bash
# /home/<user>目录权限为755才能免密登录
```