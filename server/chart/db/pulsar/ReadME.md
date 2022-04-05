```shell
CSRF_TOKEN=$(curl http://pulsar-web.cluster.com/pulsar-manager/csrf-token)
curl \
   -H 'X-XSRF-TOKEN: $CSRF_TOKEN' \
   -H 'Cookie: XSRF-TOKEN=$CSRF_TOKEN;' \
   -H "Content-Type: application/json" \
   -X PUT http://pulsar-web.cluster.com/pulsar-manager/users/superuser \
   -d '{"name": "admin", "password": "Czy.190815", "email": "username@test.org"}'
```