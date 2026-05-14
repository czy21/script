```shell
# migrate to temp bundle
find .temp -maxdepth 1 ! -path .temp -exec sh -c 'f={};r=$(basename $(realpath -m ../$f));br=$f/.temp/;cp -r $br $r' \;
# rm <target>/.temp
find -maxdepth 2 -name .temp ! -path ./.temp | xargs rm -rf
```