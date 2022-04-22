
# eck install
```shell
kubectl create -f https://download.elastic.co/downloads/eck/2.1.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.1.0/operator.yaml
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator

```


# eck uninstall
```shell
# 删除所有es资源
kubectl get namespaces --no-headers -o custom-columns=:metadata.name | xargs -n1 kubectl delete elastic --all -n
# 删除 operator
kubectl delete -f https://download.elastic.co/downloads/eck/1.8.0/operator.yaml
kubectl delete -f https://download.elastic.co/downloads/eck/1.8.0/crds.yaml
```

# login
```shell
# 获取elasticsearch https登录密码 账号为: elastic
kubectl -n big-data get secret cluster-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo
# 9200 账号: admin 密码: elasticsearch
```