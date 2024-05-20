## Git Repository
{%- for k,v in param_registry_git_repo_dict.items() %}
  - {{ k }}: [{{ v }}]({{ v }}){:target=_blank}
{%- endfor %}
{%- if param_docker_dockerfiles %}
## Dockerfile
{%- for t in param_docker_dockerfiles %}
- {{ t["name"] }}
```dockerfile
{{ t["content"] }}
```
```bash
{{ t["command"] }}
```
{%- endfor %}
{%- endif %}
{%- if param_docker_compose %}
## Docker Compose
```yaml
{{ param_docker_compose['content'] }}
```
```bash
{{ param_docker_compose['command'] }}
```
{%- endif %}