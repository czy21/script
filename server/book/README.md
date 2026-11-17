## Ubuntu pre-installed
```shell
# desktop
sudo apt install -y openssh-server sshpass vim git libfuse2 gnome-shell-extension-manager
passwd
sed -i -e "s|^PermitRootLogin.*|#\0|" -e "0,/^\S*PermitRootLogin.*/s//PermitRootLogin yes/" /etc/ssh/sshd_config
systemctl restart ssh

# set ntp server
vim /etc/systemd/timesyncd.conf
[Time]
NTP=ntp.aliyun.com

# mDNS
# sudo apt install avahi-daemon -y
```

## Ansible
```bash
# use pip
$HOME/.python3/bin/python3 -m pip install ansible
# mac
sudo brew install sshpass
# ubuntu 22.04 (jammy)
sudo apt install sshpass -y
```