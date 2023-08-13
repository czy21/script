## git repo
  - github: [https://github.com/czy21/container/tree/main/hadoop](https://github.com/czy21/container/tree/main/hadoop){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/hadoop](https://gitee.com/czy21/container/tree/main/hadoop){:target=_blank}
## dockerfile
- DockerfileBase
```bash
docker build --tag docker.io/czy21/hadoop-base --file DockerfileBase . --pull
```
- Dockerfile
```bash
docker build --tag docker.io/czy21/hadoop --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name hadoop --file deploy.yml up --detach --remove-orphans
```