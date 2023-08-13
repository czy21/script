## git repo
  - github: [https://github.com/czy21/container/tree/main/jira](https://github.com/czy21/container/tree/main/jira){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/jira](https://gitee.com/czy21/container/tree/main/jira){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/jira --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name jira --file deploy.yml up --detach --remove-orphans
```