```shell
# migrate to temp bundle
find ___temp -maxdepth 1 ! -path ___temp -exec sh -c 'f={};r=$(basename $(realpath -m ../$f));br=$f/___temp/;cp -r $br $r' \;
# rm <target>/___temp
find -maxdepth 2 -name ___temp ! -path ./___temp | xargs rm -rf
```