```shell

# init db for pgsql
#https://raw.githubusercontent.com/apache/pulsar-manager/v0.2.0/src/main/resources/META-INF/sql/postgresql-schema.sql

CSRF_TOKEN=$(curl http://pulsar-web.czy21-internal.com/pulsar-manager/csrf-token)
curl \
   -H 'X-XSRF-TOKEN: $CSRF_TOKEN' \
   -H 'Cookie: XSRF-TOKEN=$CSRF_TOKEN;' \
   -H "Content-Type: application/json" \
   -X PUT http://pulsar-web.czy21-internal.com/pulsar-manager/users/superuser \
   -d '{"name": "admin", "password": "<password>", "email": "username@test.org"}' 
```