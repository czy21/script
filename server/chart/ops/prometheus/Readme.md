```html
docker 11600 
mysql: 7362 
pgsql: 9628
node: 8919 1860
k8s: 13105
spring-metrics: 13657
```

```shell
cd ~ && git clone https://github.com/prometheus-operator/kube-prometheus.git offical-prometheus && cd offical-prometheus && git checkout tags/v0.9.0 -b v0.9.0
kubectl apply -f manifests/setup/
rm -rf manifests/prometheus-adapter-*
find manifests/prometheus-* manifests/node-exporter-* manifests/kube-state-metrics-* -exec kubectl apply -f {} \;
```