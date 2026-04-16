
## ServiceAccount永久Token
```shell
kubectl get -n ops secret argo-workflows-admin.service-account-token -o=jsonpath='{.data.token}' | base64 --decode
```
## ServiceAccount临时Token
```shell
kubectl -n ops create token argo-workflows-admin
```