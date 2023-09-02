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

https://host.czy21-internal.com:5001/webapi/entry.cgi?api=SYNO.ActiveBackup.Activation&method=set&version=1&activated=true&serial_number="serialNumber"
```
# nginx
```text
# /etc/nginx/conf.d/http.app.conf
server {
    listen       80;
    listen      443 ssl http2;
    server_name  *.czy21-internal.com;

    client_max_body_size 0;
    chunked_transfer_encoding off;

    include /usr/syno/etc/www/certificate/ReverseProxy_e2a8ddc0-8d6c-46ba-b700-60e874332cb5/cert.conf*;
    include /usr/syno/etc/security-profile/tls-profile/config/ReverseProxy_e2a8ddc0-8d6c-46ba-b700-60e874332cb5.conf*;

    location / {

        proxy_set_header Host                $host;
        proxy_set_header X-Real-IP           $remote_addr;
        proxy_set_header X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto   $scheme;

        proxy_pass http://127.0.0.1:8080;
    }
}

server {
    listen       80;
    server_name  alist.czy21-internal.com;
    return       301 https://$server_name$request_uri;
}
```