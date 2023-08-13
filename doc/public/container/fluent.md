## git repo
  - github: [https://github.com/czy21/container/tree/main/fluent](https://github.com/czy21/container/tree/main/fluent){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/fluent](https://gitee.com/czy21/container/tree/main/fluent){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/fluent --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name fluent --file deploy.yml up --detach --remove-orphans
```