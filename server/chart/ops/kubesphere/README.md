## install
```shell
kubectl create namespace kubesphere-system
-n kubesphere-system --create-namespace
```
###
default user/password (admin/P@88w0rd)
```shell
# check log
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f
# get jwt
kubectl -n kubesphere-system get cm kubesphere-config -o yaml | grep -v "apiVersion" | grep jwtSecret
# uninstall
wget https://raw.githubusercontent.com/kubesphere/ks-installer/release-3.3/scripts/kubesphere-delete.sh
# use elasticsearch 8.0: spec.es.suppressTypeName: on
```