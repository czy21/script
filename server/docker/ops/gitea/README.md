```sql
-- view push log
select 
    r.name,
    pm.remote_name,
    pm.`interval`,
    CONVERT_TZ(from_unixtime(pm.created_unix,"%Y-%m-%d %h:%i:%s"),'UTC', '+12:00') as create_time,
    CONVERT_TZ(from_unixtime(pm.last_update,"%Y-%m-%d %h:%i:%s"),'UTC', '+12:00') as update_time,
    pm.last_error
from repository r
inner join push_mirror pm on r.id = pm.repo_id
where pm.id is not null
order by r.name
```

```bash
# batch update .git/config
find -maxdepth 2 -name 'config' -exec sed -i 's|<origin>|<target>|g' {} \;
```

## FAQ
```text
待官方修复SSH_DOMAIN自动解析浏览器DOMAIN
```