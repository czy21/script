## git repo
  - github: [https://github.com/czy21/container/tree/main/confluence](https://github.com/czy21/container/tree/main/confluence){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/confluence](https://gitee.com/czy21/container/tree/main/confluence){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/confluence --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name confluence --file deploy.yml up --detach --remove-orphans
```