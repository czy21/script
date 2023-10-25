## macvlan
```shell
# ubuntu 22.04 设置网卡混杂模式
sudo ifconfig ens160 promisc
# create macvlan same net
docker network create -d macvlan --subnet=192.168.2.0/24 --gateway=192.168.2.2 --ip-range=192.168.2.10/20 -o parent=ens160 vlan20
docker run --rm -dit --network vlan20 --ip 192.168.2.17 --name macvlan-alpine1 alpine:latest ash

# 解决macvlan容器不能访问宿主机
ip link add macvlan2 link <parent interface> type macvlan mode bridge
ip addr add <macvlan interface ip> dev macvlan2
ip link set macvlan2 up
ip route add <target container ip> dev macvlan2
# 删除macvlan接口
ip link delete macvlan2
```