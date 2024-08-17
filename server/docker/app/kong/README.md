## Init DB
```shell
docker run --rm \
    -e "KONG_DATABASE=postgres" \
    -e "KONG_PG_DATABASE=kong" \
    -e "KONG_PG_HOST=<host>" \
    -e "KONG_PG_USER=<username>" \
    -e "KONG_PG_PASSWORD=<password>" \
    kong/kong-gateway:3.7.1.2 kong migrations bootstrap
```