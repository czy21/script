chmod 755 admin
bash -c "set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo python3 -m ensurepip
sudo python3 -m pip install --upgrade pip
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
# add registry
vim /var/packages/Docker/etc/dockerd.json
# restart docker
systemctl restart pkg-Docker-dockerd.service
#cd /volume1/@appstore/py3k/usr/local/lib/python3.5/site-packages
#curl -k https://bootstrap.pypa.io/pip/3.5/get-pip.py | python3
#ln -s /var/packages/py3k/target/usr/local/bin/pip3 /usr/local/bin/pip3
#ln -s /usr/local/bin/pip3 /usr/bin/pip3