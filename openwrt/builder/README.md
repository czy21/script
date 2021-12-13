```shell
git clone https://github.com/coolsnowwolf/lede
echo 'src-git helloworld https://github.com/fw876/helloworld' >> feeds.conf.default
./scripts/feeds update -a && ./scripts/feeds install -a
make menuconfig
make -j8 download V=s
# single thread
nohup make -j1 V=s &
# multi thread
nohup make -j$(($(nproc) + 1)) V=s &
```