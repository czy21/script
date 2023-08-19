## git repo
  - github: [https://github.com/czy21/container/tree/main/ubuntu-friendlywrt](https://github.com/czy21/container/tree/main/ubuntu-friendlywrt){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/ubuntu-friendlywrt](https://gitee.com/czy21/container/tree/main/ubuntu-friendlywrt){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/ubuntu-friendlywrt --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name ubuntu-friendlywrt --file deploy.yml up --detach --remove-orphans
```