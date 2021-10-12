```shell
git clone https://github.com/coolsnowwolf/lede
echo 'src-git helloworld https://github.com/fw876/helloworld' >> feeds.conf.default
./scripts/feeds update -a && ./scripts/feeds install -a
make menuconfig
make -j8 download V=s
nohup make -j1 V=s &
```