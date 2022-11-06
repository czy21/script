### install need disconnect internet

```bash
sh -c "set -e;cd;mkdir -p .ssh;chmod 700 .ssh;echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3nTRJ/aVb67l1xMaN36jmIbabU7Hiv/xpZ8bwLVvNO3Bj7kUzYTp7DIbPcHQg4d6EsPC6j91E8zW6CrV2fo2Ai8tDO/rCq9Se/64F3+8oEIiI6E/OfUZfXD1mPbG7M/kcA3VeQP6wxNPhWBbKRisqgUc6VTKhl+hK6LwRTZgeShxSNcey+HZst52wJxjQkNG+7CAEY5bbmBzAlHCSl4Z0RftYTHR3q8LcEg7YLNZasUogX68kBgRrb+jw1pRMNo7o7RI9xliDAGX+E4C3vVZL0IsccKgr90222axsADoEjC9O+Q6uwKjahemOVaau+9sHIwkelcOcCzW5SuAwkezv 805899926@qq.com > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys"
sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /var/packages/Docker/target/usr/bin/docker-compose
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
# add registry
vim /var/packages/Docker/etc/dockerd.json
# restart docker
systemctl restart pkg-Docker-dockerd.service
```

```bash
scp http.app.conf <host>:/etc/nginx/conf.d/

wget https://raw.githubusercontent.com/th0ma7/synology/master/packages/ffmpeg-4.4.1/ffmpeg_x64-7.0_4.4.1-40.spk

sudo mv /var/packages/CodecPack/target/bin/ffmpeg41 /var/packages/CodecPack/target/bin/ffmpeg41.bak
# upload ffmpeg.spk

ln /var/packages/ffmpeg/target/bin/ffmpeg /var/packages/CodecPack/target/bin/ffmpeg41
```

```shell
# active backup for business 激活
https://host:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=username&passwd=password&format= cookie

https://host.cluster.com:5001/webapi/entry.cgi?api=SYNO.ActiveBackup.Activation&method=set&version=1&activated=true&serial_number="serialNumber"
```
