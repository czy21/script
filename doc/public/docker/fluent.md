## git repo
  - github: https://github.com/czy21/container/tree/main/fluent
  - gitee: https://gitee.com/czy21/container/tree/main/fluent
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/fluent --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name fluent --file deploy.yml up --detach --remove-orphans
```