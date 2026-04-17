inputs=[:]

inputs.param_kube_credential = 'k8s-config-dev'

inputs.param_helm_repo = 'http://nexus.czy21-internal.com/repository/helm-hosted/'
inputs.param_helm_java_chart_name = "java-template"
inputs.param_helm_java_chart_version = "0.1.0"

inputs.param_helm_go_chart_name = "go-template"
inputs.param_helm_go_chart_version = "0.1.0"

inputs.param_helm_python_chart_name = "python-template"
inputs.param_helm_python_chart_version = "0.1.0"

inputs.param_helm_web_chart_name="web-template"
inputs.param_helm_web_chart_version = "0.1.0"

inputs.param_registry_repo= 'registry.czy21.com'
inputs.param_registry_dir= 'library'

inputs.param_go_proxy="http://nexus.czy21-internal.com/repository/go-proxy-group/,direct"
inputs.param_npm_repo="http://nexus.czy21-internal.com/repository/npm-group/"

return param