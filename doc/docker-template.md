{%- if param_docker_dockerfile_content %}
## dockerfile
{{ param_docker_dockerfile_content }}
{%- endif %}
{%- if param_docker_conf_dict -%}
## conf
{%- for k,v in param_docker_conf_dict.items() %}
- {{ k }}
```text
{{ v }}
```
{%- endfor %}
{%- endif %}
## docker-compose
```bash
{{ param_docker_compose_command }}
```
```yaml
{{ param_docker_compose_content }}
```