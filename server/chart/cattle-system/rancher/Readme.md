```shell
# cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.crds.yaml
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.12.0

# uninstall
kubectl apply -f https://raw.githubusercontent.com/rancher/rancher-cleanup/main/deploy/rancher-cleanup.yaml
```