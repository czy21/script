```shell
# migrate to temp bundle
find ___temp -name "*.bak" -exec sh -c 'f={};r=$(basename $(realpath -m $f/../../));br=$r/___temp/;mkdir -p $br;cp $f $br' \;
# rm ___temp
find -name ___temp | xargs rm -rf
```