
## conf
- /volume5/storage/docker-data/fluent-bit/conf/fluent-bit.conf
```text
[SERVICE]
    flush        1
    daemon       Off
    log_level    info
    parsers_file parser.conf
    plugins_file plugin.conf
    http_server  Off
    http_listen  0.0.0.0
    http_port    2020

[INPUT]
    Name forward
    Listen 0.0.0.0
    port 24224

@INCLUDE nginx.conf
```
- /volume5/storage/docker-data/fluent-bit/conf/nginx.conf
```text
[FILTER]
    name parser
    Match docker.nginx
    Key_Name log
    Parser nginx
    Preserve_Key On
    Reserve_Data On
[FILTER]
    name               log_to_metrics
    match              docker.nginx
    tag                nginx_metrics
    metric_mode        counter
    metric_name        nginx_request_total
    metric_description How many HTTP requests processed, partitioned by host, code, and method.
    label_field        host
    label_field        method
    label_field        code
[FILTER]
    name               log_to_metrics
    match              docker.nginx
    tag                nginx_metrics
    metric_mode        histogram
    metric_name        nginx_request_duration_seconds
    metric_description How long it took to process the request, partitioned by host, code, and method.
    value_field        request_time
    bucket             0.1
    bucket             0.3
    bucket             1.2
    bucket             5.0
    label_field        host
    label_field        method
    label_field        code
[FILTER]
    name               log_to_metrics
    match              docker.nginx
    tag                nginx_metrics
    metric_mode        histogram
    metric_name        nginx_upstream_duration_seconds
    metric_description How long it took to process the upstream response, partitioned by host, code, and method.
    value_field        upstream_response_time
    bucket             0.1
    bucket             0.3
    bucket             1.2
    bucket             5.0
    label_field        host
    label_field        method
    label_field        code
[OUTPUT]
    name               prometheus_exporter
    match              nginx_metrics
    host               0.0.0.0
    port               2021

[OUTPUT]
    Name  es
    match docker.nginx
    Host  <domain>
    Port  80
    HTTP_User <username>
    HTTP_Passwd <password>
    Logstash_Format On
    Logstash_Prefix fluent-nginx--log
```
- /volume5/storage/docker-data/fluent-bit/conf/parser.conf
```text
[PARSER]
    Name   nginx
    Format regex
    Regex ^(?<remote>[^ ]*) (?<host>[^ ]*) (?<user>[^ ]*) \[(?<time>[^\]]*)\] "(?<method>\S+)(?: +(?<path>[^\"]*?)(?: +\S*)?)?" (?<code>[^ ]*) (?<size>[^ ]*)(?: "(?<referer>[^\"]*)" "(?<agent>[^\"]*)"(?:\s+(?<http_x_forwarded_for>[^ ]+))?)? (?<request_time>[^ ]*) (?<upstream_response_time>[^ ]*)
    Time_Key time
    Time_Format %d/%b/%Y:%H:%M:%S %z
    Time_Keep On
    Types size:integer request_time:float upstream_response_time:float
```
- /volume5/storage/docker-data/fluent-bit/conf/plugin.conf
```text

```
## docker-compose
```bash
docker-compose --project-name fluent-bit --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

x-traefik-log-metrics-label: &traefik-log-metrics-label
  traefik.enable: true
  traefik.http.routers.fluent-bit-log-metrics.service: fluent-bit-log-metrics
  traefik.http.services.fluent-bit-log-metrics.loadbalancer.server.port: 2021

services:

  fluent-bit:
    image: fluent/fluent-bit:2.1.7
    pull_policy: always
    container_name: fluent-bit
    privileged: true
    user: root
    labels:
      <<: *traefik-log-metrics-label
    expose:
      - "2020"
      - "2021"
    ports:
      - "24224:24224" # input
      - "24224:24224/udp"
    volumes:
      - /volume5/storage/docker-data/fluent-bit/conf/:/fluent-bit/etc/
    restart: always
```