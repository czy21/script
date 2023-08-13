## git repo
  - github: https://github.com/czy21/container/tree/main/pulsar-manager
  - gitee: https://gitee.com/czy21/container/tree/main/pulsar-manager
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/pulsar-manager --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name pulsar-manager --file deploy.yml up --detach --remove-orphans
```