## init
```shell

sudo dpkg-reconfigure dash # select no sh => bash

sudo sed -i.bak -e 's|security.debian.org|mirrors.aliyun.com|g' -e 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list /etc/apt/sources.list.d/openmediavault-kernel-backports.list
sudo apt update && sudo apt upgrade -y
sudo apt install -y vim curl python3-distutils
wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash

# nfs option: async,no_root_squash,insecure_locks
# btrfs filesystem repair; cause poweroff
btrfsck --repair /dev/sdb1
```

## docker
```shell
# omv allow 2375
vim /etc/systemd/system/multi-user.target.wants/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock -H tcp://0.0.0.0:2375
# docker-compose
sudo ln -sf /usr/libexec/docker/cli-plugins/docker-compose /usr/bin/docker-compose
```