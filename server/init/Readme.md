#ansible install and config on server
must be use root !!!
```Bash
yum -y install epel-release
yum -y install ansible
sed -ir 's/^#\(host_key_checking\)/\1/' /etc/ansible/ansible.cfg
```


###!!! calico 启动 crashloopbackoff异常解决
####主节点 工作节点 均执行
```Bash
nmcli device delete br-xxx
```