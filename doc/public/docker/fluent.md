
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/fluent --file Dockerfile . --pull
```
```dockerfile
FROM fluent/fluentd:v1.16-debian
USER root

RUN gem install fluent-plugin-prometheus
RUN gem install fluent-plugin-elasticsearch -v 5.1.0
RUN gem uninstall elasticsearch elasticsearch-api elastic-transport --force -x
RUN gem install elasticsearch -v 7.17

USER fluent
```
## conf
- /volume5/storage/docker-data/fluent/conf/fluent.conf
```text
<source>
  @type  forward
  port  24224
  bind 0.0.0.0
</source>

<source>
  @type prometheus
</source>

<filter docker.nginx>
  @type parser
  key_name log
  reserve_data true
  <parse>
  @type regexp
  expression /^(?<remote>[^ ]*) (?<host>[^ ]*) (?<user>[^ ]*) \[(?<time>[^\]]*)\] "(?<method>\S+)(?: +(?<path>[^\"]*?)(?: +\S*)?)?" (?<code>[^ ]*) (?<size>[^ ]*)(?: "(?<referer>[^\"]*)" "(?<agent>[^\"]*)"(?:\s+(?<http_x_forwarded_for>[^ ]+))?)? (?<request_time>[^ ]*) (?<upstream_response_time>[^ ]*)$/
    time_format %d/%b/%Y:%H:%M:%S %z
    types size:integer,request_time:float,upstream_response_time:float
  </parse>
</filter>

<filter docker.nginx>
  @type prometheus

  <metric>
    name nginx_size_bytes_total
    type counter
    desc nginx bytes sent
    key size
    <labels>
      host   ${host}
    </labels>
  </metric>

  <metric>
    name nginx_request_code_total
    type counter
    desc nginx request code
    <labels>
      host   ${host}
      method ${method}
      path   ${path}
      code ${code}
    </labels>
  </metric>

  <metric>
    name nginx_request_duration_total_seconds
    type counter
    desc nginx request time
    key request_time
    <labels>
     host   ${host}
     method ${method}
     code ${code}
    </labels>
  </metric>
  <metric>
    name nginx_upstream_response_duration_total_seconds
    type counter
    desc nginx upstream response time
    key upstream_response_time
    <labels>
     host   ${host}
     method ${method}
     code ${code}
    </labels>
  </metric>
  <metric>
    name nginx_request_duration_seconds
    type summary
    desc nginx request duration summary
    key request_time
    <labels>
     host   ${host}
     method ${method}
     code ${code}
    </labels>
  </metric>
  <metric>
    name nginx_upstream_duration_seconds
    type summary
    desc nginx upstream duration summary
    key upstream_response_time
    <labels>
     host   ${host}
     method ${method}
     code ${code}
    </labels>
  </metric>
</filter>

<match docker.nginx>
  @type copy
  <store>
    @type elasticsearch
    host <domain>
    port 80
    user <username>
    password <password>
    logstash_format true
    logstash_prefix fluent-nginx--log
  </store>
</match>
```
## docker-compose
```bash
docker-compose --project-name fluent --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  fluent:
    image: "docker.io/czy21/fluent"
    pull_policy: always
    container_name: fluent
    privileged: true
    user: root
    ports:
      - "24224:24224" # input
      - "24224:24224/udp"
      - "24231:24231"
    expose:
      - "24231" # metrics
    volumes:
      - /volume5/storage/docker-data/fluent/conf/:/fluentd/etc/
      - /volume5/storage/docker-data/fluent/log/:/fluentd/log/
    restart: always
```