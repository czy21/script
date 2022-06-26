#
```shell

# install on centos/rhel
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install consul

# backup
consul kv export > bak.json
# restore
cat bak.json | consul kv import -token <token_value> -
# get bootstrap token
kubectl get secrets/consul-bootstrap-acl-token -n ops --template='{{.data.token | base64decode }}'
# exec container
kubectl exec consul-server-0 -n ops -it /bin/sh
consul kv delete -token <token_value> -recurse <key>
```