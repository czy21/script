#ansible install and config on server
must be use root !!!
```shell
yum -y install epel-release
yum -y install ansible
sed -ir 's/^#\(host_key_checking\)/\1/' /etc/ansible/ansible.cfg
```

### calico 启动 crashloopbackoff 异常解决
```shell
# 主节点 工作节点 均执行
nmcli device delete br-xxx
# 主节点 删除calico pod
kubectl delete pod calico-node-xxxxx -n kube-system
```
###创建NFS StorageClass
```shell
# 下载所需文件
mkdir nfs-client && for file in class.yaml deployment.yaml rbac.yaml ; do wget -P nfs-client  https://raw.githubusercontent.com/kubernetes-incubator/external-storage/master/nfs-client/deploy/$file; done
# 修改 deployment.yaml 中的两处 NFS 服务器 IP 和目录

# 部署
kubectl apply -f rbac.yaml,class.yaml,deployment.yaml
# 标记默认 StorageClass
kubectl patch storageclass managed-nfs-storage -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

###部署kubeSphere 默认帐户和密码 (admin/P@88w0rd)
```shell
kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/v3.1.0/kubesphere-installer.yaml
kubectl apply -f https://github.com/kubesphere/ks-installer/releases/download/v3.1.0/cluster-configuration.yaml
# 检查安装日志
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f
# 检查状态
kubectl get svc/ks-console -n kubesphere-system

# /etc/kubernetes/manifests/kube-apiserver.yaml command 下添加 - --feature-gates=RemoveSelfLink=false
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