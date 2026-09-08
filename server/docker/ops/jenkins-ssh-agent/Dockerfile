FROM jenkins/ssh-agent:{{ param_role_version }}

USER root
RUN apt-get update -y && apt-get install -y lsb-release git curl
RUN install -m 0755 -d /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && chmod a+r /etc/apt/keyrings/docker.asc
RUN tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(lsb_release -cs)
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
RUN apt-get update -y
RUN docker_version=`apt-cache madison docker-ce | awk '{ print $3 }' | grep "{{ param_docker_version }}" | head -n 1`;apt-get install -y docker-ce-cli=${docker_version}
RUN ln -sf /usr/libexec/docker/cli-plugins/docker-compose /usr/bin/docker-compose