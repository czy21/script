```shell
# migrate to temp bundle
find ___temp -maxdepth 1 ! -path ___temp -exec sh -c 'f={};r=$(basename $(realpath -m ../$f));br=$f/___temp/;cp -r $br $r' \;
# rm <target>/___temp
find -maxdepth 2 -name ___temp ! -path ./___temp | xargs rm -rf
```
## docker compose
```shell
curl -SL "https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/lib/docker/cli-plugins/docker-compose
chmod +x /usr/lib/docker/cli-plugins/docker-compose
ln -sf /usr/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose
```