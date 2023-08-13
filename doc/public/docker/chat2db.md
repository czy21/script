## git repo
  - github: [https://github.com/czy21/container/tree/main/chat2db](https://github.com/czy21/container/tree/main/chat2db){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/chat2db](https://gitee.com/czy21/container/tree/main/chat2db){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/chat2db --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name chat2db --file deploy.yml up --detach --remove-orphans
```