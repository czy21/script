param=[:]
param.param_kube_credential = 'k8s-config-dev'

param.param_helm_repo = 'http://nexus.czy21.com/repository/helm-hosted/'
param.param_helm_java_chart_name = "java-template"
param.param_helm_java_chart_version = "0.1.0"

param.param_helm_go_chart_name = "go-template"
param.param_helm_go_chart_version = "0.1.0"

param.param_helm_python_chart_name = "python-template"
param.param_helm_python_chart_version = "0.1.0"

param.param_helm_web_chart_name="web-template"
param.param_helm_web_chart_version = "0.1.0"

param.param_registry_repo= 'registry.czy21.com'
param.param_registry_dir= 'library'

param.param_go_proxy="http://nexus.czy21.com/repository/go-proxy-group/,direct"
param.param_npm_repo="http://nexus.czy21.com/repository/npm-group/"

return param