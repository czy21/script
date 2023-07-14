
## dockerfile
- Dockerfile
```bash
docker build --tag registry.czy21-public.com/library/jenkins-ssh-agent --file Dockerfile . --pull
```
```dockerfile
FROM jenkins/ssh-agent:5.1.0-jdk17
USER root
RUN apt update && apt install git sudo curl -y
RUN curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
RUN echo -n "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-custom
RUN usermod -aG sudo jenkins
```
## docker-compose
```bash
docker-compose --project-name jenkins-ssh-agent --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"

services:

  jenkins-ssh-agent:
    image: registry.czy21-public.com/library/jenkins-ssh-agent
    pull_policy: always
    container_name: jenkins-ssh-agent
    privileged: true
    ports:
      - "5022:22"
    volumes:
      - /volume5/storage/docker-data/jenkins-ssh-agent/data/:/home/jenkins/
      - /volume5/storage/docker-data/jenkins-ssh-agent/data/.jenkins:/home/jenkins/.jenkins
      - /volume5/storage/docker-data/jenkins-ssh-agent/data/agent:/home/jenkins/agent
      - /run/:/run/
      - /var/run/:/var/run/
      - /tmp/:/tmp/
    environment:
      JENKINS_AGENT_SSH_PUBKEY: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDNiu2EIXk3id8QagrKhcHqzdGPzjE0oLag1lAMK/oBT3nidQb9o7Cprj+iJeeghWw3NjcFHppMmzzmnzI7lseiVZ0s/tgH6qBAozUkIqHFROKvnMi0oQ/oVBqgRVAO8tVLjou31e6DB4ru3ycBEnNZXj2Z+6CPvZc7s4LuTdvgnJFgPPBWYKzqMh0BsWFskO72tjkd3SrIA0KL36Ezy/e82g2qozCISO+X3Y7lnWqP9WRuAzWLwm24iH01X5/EdkfupW6pDsrA8PwHnbFMvNBEaCQZpEk3Nbw5pg6lMYfZX6q4wzqFnrS6A2zFKgZuT/PcptTxhuDQsbyEf4hcJMCXuHRHWsnNYqmtffEenydYojcLK7cWSDifq7gqci/SpmUTC8VlSYLHwL6AFLAoAOez7Zq5+wGlUaqZ4tddZ4dLRlMLL0ZQi5N0tDbmvkSKDjkJSGJcEbpR6/hcvDqmuPcttb26X0jc0HeEApx2+cWOnD9BUxTVSAOqD2kzLIAsitE= 805899926@qq.com
    restart: always
```