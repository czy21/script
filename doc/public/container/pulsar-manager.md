## git repo
  - github: [https://github.com/czy21/container/tree/main/pulsar-manager](https://github.com/czy21/container/tree/main/pulsar-manager){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/pulsar-manager](https://gitee.com/czy21/container/tree/main/pulsar-manager){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/pulsar-manager --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name pulsar-manager --file deploy.yml up --detach --remove-orphans
```