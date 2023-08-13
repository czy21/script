## git repo
  - github: [https://github.com/czy21/container/tree/main/kafka](https://github.com/czy21/container/tree/main/kafka){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/kafka](https://gitee.com/czy21/container/tree/main/kafka){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/kafka --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name kafka --file deploy.yml up --detach --remove-orphans
```