#
```shell
# backup
consul kv export > bak.json
# restore
cat bak.json | consul kv import -
```