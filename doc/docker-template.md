# dockerfile

{%- if param_docker_conf_content %}
# conf
{%- for k,v in param_docker_conf_content.items() %}
- {{ k }}
```text
{{ v }}
```
{%- endfor %}
{%- endif %}

# docker-compose
```shell
{{ param_docker_compose_command }}
```
```yaml
{{ param_docker_compose_content }}
```