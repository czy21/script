## git repo
  - github: https://github.com/czy21/container/tree/main/flink
  - gitee: https://gitee.com/czy21/container/tree/main/flink
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/flink --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name flink --file deploy.yml up --detach --remove-orphans
```