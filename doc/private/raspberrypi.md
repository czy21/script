## init 
```shell
# edit static ip
sudo nano /etc/dhcpcd.conf
interface wlan0
static ip_address=192.168.2.11/24
static routes=192.168.2.2
# install pip3
sudo apt-get install -y python3-pip
# install docker-compose
sudo pip3 install docker-compose
```
## install
```shell
# docker
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
# webadmin
wget http://prdownloads.sourceforge.net/webadmin/webmin_1.990_all.deb
sudo apt-get install libnet-ssleay-perl  libauthen-pam-perl libio-pty-perl shared-mime-info
sudo apt --fix-broken install
sudo dpkg --install webmin_1.990_all.deb
```

# remark
注: usb口插入otg失效,应接power口