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

###
kubeSphere default user/password (admin/P@88w0rd)
```shell
kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/v3.1.0/kubesphere-installer.yaml
kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/v3.1.0/cluster-configuration.yaml
# check log
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f

# check status
kubectl get svc/ks-console -n kubesphere-system

# uninstall
wget https://raw.githubusercontent.com/kubesphere/ks-installer/release-3.1/scripts/kubesphere-delete.sh
```

### join cluster
```shell
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