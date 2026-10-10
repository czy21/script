#!/bin/bash
set -e

mkdir -p .jenkins/docker

cat > .jenkins/docker/ssh_config <<EOF
Host docker-remote
    HostName ${SSH_HOST}
    User ${SSH_USER}
    IdentityFile ${SSH_FILE}
    IdentitiesOnly yes
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
EOF

cat > .jenkins/docker/ssh <<'EOF'
#!/bin/bash
exec /usr/bin/ssh -F .jenkins/docker/ssh_config "$@"
EOF

chmod +x .jenkins/docker/ssh

export PATH="$PWD/.jenkins/docker:$PATH"
export DOCKER_HOST=ssh://docker-remote