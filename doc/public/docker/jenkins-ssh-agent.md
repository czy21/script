## git repo
  - github: [https://github.com/czy21/container/tree/main/jenkins-ssh-agent](https://github.com/czy21/container/tree/main/jenkins-ssh-agent){:target=_blank}
  - gitee: [https://gitee.com/czy21/container/tree/main/jenkins-ssh-agent](https://gitee.com/czy21/container/tree/main/jenkins-ssh-agent){:target=_blank}
## dockerfile
- Dockerfile
```bash
docker build --tag docker.io/czy21/jenkins-ssh-agent --file Dockerfile . --pull
```
## docker-compose
```bash
docker-compose --project-name jenkins-ssh-agent --file deploy.yml up --detach --remove-orphans
```