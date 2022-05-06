```shell
# kong init db
docker run --rm \
    -e "KONG_DATABASE=postgres" \
    -e "KONG_PG_HOST=192.168.2.18" \
    -e "KONG_PG_USER=postgres" \
    -e "KONG_PG_PASSWORD=***REMOVED***" \
    -e "KONG_CASSANDRA_CONTACT_POINTS=kong" \
    kong/kong-gateway:2.8-alpine kong migrations bootstrap
# konga init db
docker run --rm pantsel/konga:latest -c prepare -a mysql -u "mysql://admin:***REMOVED***@192.168.2.18:3306/konga"
```