# ansible install and config on server
## centos
```shell
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
# allow master taint
kubectl taint nodes --all node-role.kubernetes.io/master-
# get join command on master node
kubeadm token create --print-join-command
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