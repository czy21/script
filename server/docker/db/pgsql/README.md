# Create Extension
```sql
CREATE EXTENSION "uuid-ossp";
```

# Conf pg_hba.conf 允许任意地址访问
```text
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             0.0.0.0/0               md5
```

# User
## Create User and set role
```sql
CREATE USER <username> WITH PASSWORD '<password>';
alter role <username> superuser;
drop role <username>;
```