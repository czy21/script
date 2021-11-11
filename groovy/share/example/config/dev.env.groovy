env.param_kube_credential = 'kube-config-dev'
env.param_kube_server = 'https://192.168.2.21:6443'

env.param_helm_repo = 'http://nexus.cluster.com/repository/helm/'
env.param_helm_java_chart_name = "java-template"
env.param_helm_java_chart_version = "0.1.0"

env.param_registry_repo= 'registry.cluster.com:8080'
env.param_registry_dir= 'library'
env.param_registry_username = 'admin'
env.param_registry_password = '***REMOVED***'

env.param_helm_web_chart_name="web-template"
env.param_helm_web_chart_version = "0.1.0"