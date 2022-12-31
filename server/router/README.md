```base
# migrate to temp bundle
find ___temp -name "*.bak" -exec sh -c 'f={};r=$(basename $(realpath $f/../../));br=$r/___temp/;mkdir -p $br;cp $f $br' \;
```