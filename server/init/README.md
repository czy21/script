## Ubuntu pre-installed
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

## Ansible
```bash
# use pip
$HOME/.python3/bin/python3 -m pip install ansible
# ubuntu 22.04 (jammy)
sudo apt install sshpass -y
```

### Kubernetes
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