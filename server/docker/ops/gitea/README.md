```sql
-- view push log
select 
    r.name,
    pm.`interval`,
    CONVERT_TZ(from_unixtime(pm.created_unix,"%Y-%m-%d %h:%i:%s"),'UTC', '+12:00') as create_time,
    CONVERT_TZ(from_unixtime(pm.last_update,"%Y-%m-%d %h:%i:%s"),'UTC', '+12:00') as update_time
from repository r
inner join push_mirror pm on r.id = pm.repo_id
where pm.id is not null
```