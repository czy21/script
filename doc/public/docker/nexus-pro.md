## git repo
  - github: https://github.com/czy21/container/tree/main/nexus-pro
  - gitee: https://gitee.com/czy21/container/tree/main/nexus-pro
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/nexus-pro --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name nexus-pro --file deploy.yml up --detach --remove-orphans
```