#!/bin/bash
set -e

sudo systemctl stop gitea-runner || true

sudo wget -nv -O /usr/local/bin/gitea-runner https://dl.gitea.com/gitea-runner/{{ param_gitea_runner_version }}/gitea-runner-{{ param_gitea_runner_version }}-linux-amd64
sudo chown root:root /usr/local/bin/gitea-runner && sudo chmod +x /usr/local/bin/gitea-runner
sudo ln -sf /usr/local/bin/gitea-runner /usr/bin/gitea-runner

(
    cd
    rm -f .runner*
    gitea-runner register --no-interactive --instance {{ param_gitea_instance_url }} --token {{ param_gitea_runner_token }} --name $(hostname) --labels {{ param_gitea_runner_label }},self-hosted:host
)

sudo tee /etc/systemd/system/gitea-runner.service << EOF
[Unit]
Description=Gitea Actions runner
Documentation=https://gitea.com/gitea/runner
After=network-online.target
Wants=network-online.target
# Uncomment when jobs use the local Docker daemon:
# After=docker.service
# Requires=docker.service

[Service]
Type=simple
ExecStart=/usr/local/bin/gitea-runner daemon --config /etc/gitea-runner/config.yaml
WorkingDirectory=$HOME
User=$USER
Group=$USER
Restart=on-failure
RestartSec=5s
# Allow running jobs to finish before the runner is stopped. Keep this in sync
# with runner.shutdown_timeout in the config.
TimeoutStopSec=3h

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now gitea-runner