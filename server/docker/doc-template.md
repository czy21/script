## Git Repository
{%- for k,v in param_registry_git_repo_dict.items() %}
  - {{ k }}: [{{ v }}]({{ v }}){:target=_blank}
{%- endfor %}
{%- if param_docker_dockerfile_dict %}
## Dockerfile
{%- for k,v in param_docker_dockerfile_dict.items() %}
```dockerfile
{{ v["content"] }}
```
```bash
{{ v["command"] }}
```
{%- endfor %}
{%- endif %}
{%- if param_docker_compose_command %}
## Docker Compose
```yaml
{{ param_docker_compose_content }}
```
```bash
{{ param_docker_compose_command }}
```
{%- endif %}