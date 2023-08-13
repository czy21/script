## git repo
  - github: https://github.com/czy21/container/tree/main/confluence
  - gitee: https://gitee.com/czy21/container/tree/main/confluence
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/confluence --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name confluence --file deploy.yml up --detach --remove-orphans
```