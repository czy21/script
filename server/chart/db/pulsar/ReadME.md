```shell

# init db for pgsql
#https://raw.githubusercontent.com/apache/pulsar-manager/v0.3.0/src/main/resources/META-INF/sql/postgresql-schema.sql

CSRF_TOKEN=$(curl http://pulsar-web.cluster.com/pulsar-manager/csrf-token)
curl \
   -H 'X-XSRF-TOKEN: $CSRF_TOKEN' \
   -H 'Cookie: XSRF-TOKEN=$CSRF_TOKEN;' \
   -H "Content-Type: application/json" \
   -X PUT http://pulsar-web.cluster.com/pulsar-manager/users/superuser \
   -d '{"name": "admin", "password": "***REMOVED***", "email": "username@test.org"}'
```