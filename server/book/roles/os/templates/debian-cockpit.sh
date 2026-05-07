#!/bin/bash
set -e

# . /etc/os-release
# sudo apt install -t ${VERSION_CODENAME}-backports cockpit

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://repo.45drives.com/key/gpg.asc -o /etc/apt/keyrings/45drives.asc
sudo chmod a+r /etc/apt/keyrings/45drives.asc

echo "deb [signed-by=/etc/apt/keyrings/45drives.asc] https://repo.45drives.com/enterprise/debian bookworm main" | sudo tee /etc/apt/sources.list.d/45drives.list

sudo apt-get -y install cockpit-file-sharing