 #!/bin/bash

set -e

local_ip=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1 -d '/')

sudo wget https://storage.googleapis.com/harbor-releases/release-1.7.0/harbor-offline-installer-v1.7.4.tgz -O - | sudo tar -zxvf - -C /usr/local/lib/
sudo sed -i -r "s/^\s*hostname\s=\s+reg.mydomain.com/hostname = $local_ip/;s/^\s*harbor_admin_password\s=\s+Harbor12345/harbor_admin_password = admin/;" /usr/local/lib/harbor/harbor.cfg
sudo /usr/local/lib/harbor/prepare
sudo /usr/local/lib/harbor/install.sh

