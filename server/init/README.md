## centos pre-installed
```shell
sudo yum -y install tar wget epel-release 
sudo yum -y update
sudo yum -y install ansible
```
## ubuntu pre-installed
```shell
# desktop
sudo apt install -y openssh-server sshpass vim git libfuse2 gnome-shell-extension-manager
passwd
sed -i -e "s|^PermitRootLogin.*|#\0|" -e "0,/^\S*PermitRootLogin.*/s//PermitRootLogin yes/" /etc/ssh/sshd_config

# set ntp server
vim /etc/systemd/timesyncd.conf
[Time]
NTP=ntp.aliyun.com

# mDNS
# sudo apt install avahi-daemon -y
```
## ansible
```bash
# debian 11
echo 'deb http://ppa.launchpad.net/ansible/ansible/ubuntu focal main' > /etc/apt/sources.list.d/ansible.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
sudo apt install ansible

# ubuntu 22.04 (jammy)
#sudo update-alternatives --list python
#sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
#sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.10 2
#sudo update-alternatives --config python # 1
#sudo apt install software-properties-common -y
#sudo add-apt-repository ppa:ansible/ansible --yes --update
sudo apt install ansible sshpass -y
```

### docker
```shell
# allow user exec docker
sudo usermod -aG docker $USER

# ubuntu cri-dockerd
wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.2.5/cri-dockerd_0.2.5.3-0.ubuntu-$(lsb_release -c -s)_amd64.deb -O cri-dockerd.deb && sudo dpkg -i cri-dockerd.deb && rm -rf cri-dockerd.deb

# remote access with daemon.json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://127.0.0.1:2375"]
}
```

### k8s
```shell
# get join command on master node
sudo kubeadm token create --print-join-command

# get certificate-key will be deleted in two hours
sudo kubeadm init phase upload-certs --upload-certs
# join master as master: [join-command] --control-plane --certificate-key [certificate-key]
# join master as worker: [join-command]

# allow master scheduling
kubectl taint node --selector='node-role.kubernetes.io/control-plane' node-role.kubernetes.io/control-plane- node-role.kubernetes.io/master-

# deny master scheduling
kubectl taint node --selector='node-role.kubernetes.io/control-plane' node-role.kubernetes.io/control-plane="":NoSchedule node-role.kubernetes.io/master="":NoSchedule

# add label to node
kubectl label nodes k8s-nodeX slave=X

# show node label
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

### velero
```shell
# guide: https://velero.io/docs/v1.10/migration-case/
velero -n ops backup-location get
# create  backup on cluster_src
velero -n ops backup create <BACKUP_NAME> --include-namespaces stable,istio-system
# restore backup on cluster_dst
velero -n ops restore create --from-backup <BACKUP_NAME>
```