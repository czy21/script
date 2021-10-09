#
```shell
# backup
consul kv export -token [token_value] > bak.json
# restore
cat bak.json | consul kv import -token [token_value] -
# get bootstrap token
kubectl get secrets/consul-bootstrap-acl-token -n ops --template='{{.data.token | base64decode }}'
# exec container
kubectl exec consul-server-0 -n ops -it /bin/sh
```