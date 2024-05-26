## Init
```shell
sudo dpkg-reconfigure dash # select no sh => bash
sudo sed -i.bak -e 's|security.debian.org|mirrors.aliyun.com|g' -e 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list /etc/apt/sources.list.d/openmediavault-kernel-backports.list
sudo apt update && sudo apt upgrade -y
sudo apt install -y vim curl python3-distutils
wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash
```
## Docker Install
```shell
# Under SYSTEM > OMV-EXTRAS Click on the DOCKER REPO button and click on the SAVE button. 
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin

## Other
```shell
# nfs option: async,no_root_squash,insecure_locks
# btrfs filesystem repair; cause poweroff
btrfsck --repair /dev/sdb1
```