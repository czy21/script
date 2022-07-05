```base
# migrate to temp bundle
find ___temp -name "*.uci.bak" -exec sh -c 'f={};r=$(basename $f .uci.bak);br=___temp/restore;mkdir -p $br;cat $f > $br/$r.uci' \;
```