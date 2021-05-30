#ansible install and config on server
must be use root !!!
```Bash
yum -y install epel-release
yum -y install ansible
sed -ir 's/^#\(host_key_checking\)/\1/' /etc/ansible/ansible.cfg
```
