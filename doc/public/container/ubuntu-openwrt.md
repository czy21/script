## git repo
  - github: [https://github.com/czy21/container/tree/main/ubuntu-openwrt](https://github.com/czy21/container/tree/main/ubuntu-openwrt){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/ubuntu-openwrt](https://gitee.com/czy21/container/tree/main/ubuntu-openwrt){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/ubuntu-openwrt --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name ubuntu-openwrt --file deploy.yml up --detach --remove-orphans
```