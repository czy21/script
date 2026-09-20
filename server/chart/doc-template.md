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
{%- if param_k8s_helm_command %}
## Helm
```bash
{{ param_k8s_helm_command }}
```
{%- endif %}