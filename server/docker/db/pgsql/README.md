# Create Extension
```sql
CREATE EXTENSION "uuid-ossp";
```

# Create User
```sql
CREATE USER <username> WITH PASSWORD '<password>';
alter role <username> superuser;
drop role <username>;
```