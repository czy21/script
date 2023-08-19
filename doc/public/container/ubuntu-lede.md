## git repo
  - github: [https://github.com/czy21/container/tree/main/ubuntu-lede](https://github.com/czy21/container/tree/main/ubuntu-lede){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/ubuntu-lede](https://gitee.com/czy21/container/tree/main/ubuntu-lede){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/ubuntu-lede --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name ubuntu-lede --file deploy.yml up --detach --remove-orphans
```