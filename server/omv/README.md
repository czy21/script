## init
```shell

sudo dpkg-reconfigure dash # select no sh => bash

sudo sed -i.bak -e 's|security.debian.org|mirrors.aliyun.com|g' -e 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list /etc/apt/sources.list.d/openmediavault-kernel-backports.list
sudo apt update && sudo apt upgrade -y
sudo apt install -y vim curl apparmor apparmor-utils python3-venv
wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash

# nfs option: async,no_root_squash,insecure_locks
# btrfs filesystem repair; cause poweroff
btrfsck --repair /dev/sdb1
```