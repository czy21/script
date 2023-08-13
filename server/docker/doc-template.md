## git repo
{%- for k,v in param_registry_git_repo_dict.items() %}
  - {{ k }}: [{{ v }}]({{ v }}){:target=_blank}
{%- endfor %}
{%- if param_docker_dockerfile_dict %}
## dockerfile
{%- for k,v in param_docker_dockerfile_dict.items() %}
- {{ k }}
```bash
{{ v["command"] }}
```
{%- endfor %}
{%- endif %}
{%- if param_docker_compose_command %}
## docker-compose
```bash
{{ param_docker_compose_command }}
```
{%- endif %}