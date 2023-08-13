## git repo
  - github: https://github.com/czy21/container/tree/main/frp
  - gitee: https://gitee.com/czy21/container/tree/main/frp
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/frp --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name frp --file deploy.yml up --detach --remove-orphans
```