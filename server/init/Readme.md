# ansible install and config on server
## centos
```shell
sudo hostnamectl set-hostname --static [hostname]
sudo yum -y install epel-release 
sudo yum -y update
sudo yum -y install ansible
```
## ubuntu
```shell
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
sudo sed -ir 's/^#\(host_key_checking\)/\1/' /etc/ansible/ansible.cfg
```
## debian 11
```bash
echo 'deb http://ppa.launchpad.net/ansible/ansible/ubuntu focal main' > /etc/apt/sources.list.d/ansible.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
sudo apt install ansible
```
## ubuntu pre-installed 
```shell
passwd
sed -i -r "s/^\s*PermitRootLogin\s+\w+/PermitRootLogin yes/;" /etc/ssh/sshd_config
```

## mount
```shell
showmount -e [host]
# vim fstab append
[host]:/volume1/ubuntu /volume1 nfs defaults 0 0
```

### join cluster
```shell
# allow master scheduling
kubectl taint nodes --all node-role.kubernetes.io/control-plane- node-role.kubernetes.io/master-

# deny master scheduling
kubectl taint node [master host] node-role.kubernetes.io/master="":NoSchedule

# get join command on master node
sudo kubeadm token create --print-join-command
```
### kubectl for non-root user
```shell
mkdir -p $HOME/.kube && sudo cp --force /etc/kubernetes/admin.conf $HOME/.kube/config && sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### add label to node
```shell
kubectl label nodes k8s-nodeX slave=X
```
### show label
```shell
kubectl get node --show-labels
```

### k8s upgrade
```shell
# all
sudo yum install -y kubeadm-1.23.3-0 --disableexcludes=kubernetes
# master
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.23.3 --force

yum install -y kubelet-1.23.3-0 kubectl-1.23.3-0 --disableexcludes=kubernetes
sudo systemctl daemon-reload && sudo systemctl restart kubelet
```