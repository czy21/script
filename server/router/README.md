```base
# migrate to temp bundle
find ___temp -name "*.uci.bak" -exec sh -c 'f={};r=$(basename $f .uci.bak);br=$r/___temp/;mkdir -p $br;cat $f > $br/$r.uci' \;
```