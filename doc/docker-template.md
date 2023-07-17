{%- if param_docker_dockerfile_dict %}
## dockerfile
{%- for k,v in param_docker_dockerfile_dict.items() %}
- {{ k }}
```bash
{{ v["command"] }}
```
```dockerfile
{{ v["content"] }}
```
{%- endfor %}
{%- endif %}
{%- if param_docker_conf_dict %}
## conf
{%- for k,v in param_docker_conf_dict.items() %}
- {{ k }}
```{{ v["fileType"] }}
{{ v["content"] }}
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