# {{ param_role_name }}
- {{ param_registry_git_repo }}
{%- if param_repositories %}
{%- for t in param_repositories %}
- [{{ t["name"] }}:{{ t["version"] }}]({{ t['repository'] }})
{%- endfor %}
{%- endif %}
{%- if param_role_build %}
## Build
{%- for t in param_role_build %}
- [{{ t["name"] }}]({{ t['rawUrl'] }})
```bash
{{ t["command"] }}
```
{%- endfor %}
{%- endif %}
{%- if param_role_install %}
## Install
- [{{ param_role_install['name'] }}]({{ param_role_install['rawUrl'] }})
```bash
{{ param_role_install['command'] }}
```
{%- endif %}