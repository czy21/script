## Install Gateway API
```shell
kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.5.1/standard-install.yaml
```
## Add Gateway
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: nginx
  namespace: ops
spec:
  gatewayClassName: nginx
  listeners:
    - allowedRoutes:
        namespaces:
          from: All
      name: http
      port: 80
      protocol: HTTP
    - allowedRoutes:
        namespaces:
          from: All
      name: https
      port: 443
      protocol: HTTPS
      tls:
        certificateRefs:
          - name: czy21.com-secret
            kind: Secret
          - name: cf-czy21.net-secret
            kind: Secret
```
## Http to Https
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: http-to-https
  namespace: ops
spec:
  parentRefs:
    - group: gateway.networking.k8s.io
      kind: Gateway
      name: nginx
      namespace: ops
      sectionName: http
  rules:
    - filters:
        - requestRedirect:
            scheme: https
            statusCode: 301
          type: RequestRedirect
      matches:
        - path:
            type: PathPrefix
            value: /
```
## Add HttpRoute
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app1
  namespace: stable
spec:
  hostnames:
    - app1.xxx.com
  parentRefs:
    - name: nginx
      namespace: ops
  rules:
    - backendRefs:
      - name: app1
        port: 80
      matches:
      - path:
          type: PathPrefix
          value: /
```