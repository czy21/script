#!/bin/bash
set -e

sudo wget -nv -O /usr/local/bin/sops https://github.com/getsops/sops/releases/download/v{{ param_sops_version }}/sops-v{{ param_sops_version }}.linux.amd64
sudo chown root:root /usr/local/bin/sops && sudo chmod +x /usr/local/bin/sops
sudo ln -sf /usr/local/bin/sops /usr/bin/sops