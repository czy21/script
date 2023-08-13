## git repo
  - github: [https://github.com/czy21/container/tree/main/nexus-pro](https://github.com/czy21/container/tree/main/nexus-pro){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/nexus-pro](https://gitee.com/czy21/container/tree/main/nexus-pro){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/nexus-pro --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name nexus-pro --file deploy.yml up --detach --remove-orphans
```