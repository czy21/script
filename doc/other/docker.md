```shell
# ubuntu 22.04 设置网卡混杂模式
sudo ifconfig ens160 promisc
# create macvlan
docker network create -d macvlan --subnet=192.168.2.0/24 --ip-range=192.168.2.100/25 --gateway=192.168.2.132 -o parent=ens160 macvlan100
```