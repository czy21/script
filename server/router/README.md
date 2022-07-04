```base
# migrate to temp bundle
find ___temp -name "*.uci.bak" -exec sh -c 'f={};r=$(basename $f .uci.bak);br=___temp/bundle/$r;mkdir -p $br;cat $f > $br/script.uci' \;
```