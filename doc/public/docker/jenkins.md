## git repo
  - github: https://github.com/czy21/container/tree/main/jenkins
  - gitee: https://gitee.com/czy21/container/tree/main/jenkins
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/jenkins --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name jenkins --file deploy.yml up --detach --remove-orphans
```