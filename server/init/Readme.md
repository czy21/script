# ansible install and config on server
## centos
```shell
sudo yum -y install epel-release
sudo yum -y install ansible
sudo sed -ir 's/^#\(host_key_checking\)/\1/' /etc/ansible/ansible.cfg
```
## ubuntu
```shell
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
sudo sed -ir 's/^#\(host_key_checking\)/\1/' /etc/ansible/ansible.cfg
```

# ubuntu install finished prepare
```shell
passwd
sed -i -r "s/^\s*PermitRootLogin\s+\w+/PermitRootLogin yes/;" /etc/ssh/sshd_config
```

### 集群初始化后的手动执行
```shell
# 解决nfs挂载的unexpected error getting claim reference: selfLink was empty 异常
/etc/kubernetes/manifests/kube-apiserver.yaml command 下添加 - --feature-gates=RemoveSelfLink=false
# 更改nodePort范围
/etc/kubernetes/manifests/kube-apiserver.yaml command 下添加 - --service-node-port-range=1-65535
```

###
部署kubeSphere 默认帐户和密码 (admin/P@88w0rd)
```shell
kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/v3.1.0/kubesphere-installer.yaml
kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/v3.1.0/cluster-configuration.yaml
# 检查安装日志
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f
# 检查状态
kubectl get svc/ks-console -n kubesphere-system

# 卸载
wget https://raw.githubusercontent.com/kubesphere/ks-installer/release-3.1/scripts/kubesphere-delete.sh
```

### 加入集群
```shell
# 主节点 获取加入节点token
kubeadm token create --print-join-command
```
### 非root用户使用kubectl
```shell
mkdir -p $HOME/.kube && sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config && sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### 节点添加标签
```shell
kubectl label nodes k8s-nodex slave=x
```
### 查看标签
```shell
kubectl get node --show-labels
```