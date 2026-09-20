# {{ param_role_name }}
## Git Repository
{%- for k,v in param_registry_git_repo_dict.items() %}
- [{{ k }}]({{ v }})
{%- endfor %}
{%- if param_repositories %}
## Repositories
{%- for t in param_repositories %}
- [{{ t["name"] }}:{{ t["version"] }}]({{ t['repository'] }})
{%- endfor %}
{%- endif %}
{%- if param_docker_dockerfiles %}
## Dockerfile
{%- for t in param_docker_dockerfiles %}
- [{{ t["name"] }}]({{ t['rawUrl'] }})
```bash
{{ t["command"] }}
```
{%- endfor %}
{%- endif %}
{%- if param_docker_compose %}
## Docker Compose
- [{{ param_docker_compose['name'] }}]({{ param_docker_compose['rawUrl'] }})
```bash
{{ param_docker_compose['command'] }}
```
{%- endif %}