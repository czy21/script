## git repo
  - github: [https://github.com/czy21/container/tree/main/kafka-eagle](https://github.com/czy21/container/tree/main/kafka-eagle){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/kafka-eagle](https://gitee.com/czy21/container/tree/main/kafka-eagle){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/kafka-eagle --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name kafka-eagle --file deploy.yml up --detach --remove-orphans
```