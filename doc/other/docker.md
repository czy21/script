```shell
# ubuntu 22.04 设置网卡混杂模式
sudo ifconfig ens160 promisc
# create macvlan
docker network create -d macvlan --subnet=192.168.5.0/24 --gateway=192.168.5.1 -o parent=ens192 vlan5
```