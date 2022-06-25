## init
```shell

sudo dpkg-reconfigure dash # select no sh => bash

sudo sed -i.bak -e 's|security.debian.org|mirrors.aliyun.com|g' -e 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list /etc/apt/sources.list.d/openmediavault-kernel-backports.list
sudo apt update && sudo apt upgrade
sudo apt install vim python3-pip
wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash

# nfs option
async,no_root_squash,insecure_locks

# pull
rsync --archive rsync://[user]@[host]:[remote_path] [local_path] --verbose
```