#!/bin/bash
set -e

os_distribution="{{ param_ansible_distribution }}"
os_major_version="{{ param_ansible_distribution_major_version }}"

rpm_dir=

if [ "rocky" = "${os_distribution}" ]; then
  rpm_dir="${os_distribution}linux${os_major_version}"
fi

sudo tee /etc/yum.repos.d/redis.repo << EOF
[Redis]
name=Redis
baseurl=https://packages.redis.io/rpm/$rpm_dir
enabled=1
gpgcheck=1
gpgkey=https://packages.redis.io/gpg
EOF

if [ "{{ param_mirror_use_proxy | lower }}" = true ];then
  sudo cp -rv /etc/yum.repos.d/redis.repo /etc/yum.repos.d/redis.repo.bak
  sed -e "s|https://packages.redis.io/rpm|https://{{ param_mirror_raw }}/redis/rpm|g" /etc/yum.repos.d/redis.repo.bak | sudo tee /etc/yum.repos.d/redis.repo
fi

sudo yum -y install redis-{{ param_db_redis_version }}
sudo systemctl daemon-reload && sudo systemctl enable redis && sudo systemctl restart redis