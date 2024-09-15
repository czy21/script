#
```shell
# backup
consul kv export -token [token_value] > bak.json
# restore
cat bak.json | consul kv import -token [token_value] -
# get bootstrap token
kubectl get secrets/consul-bootstrap-acl-token --template='{{.data.token | base64decode }}' -n ops
```