#!/bin/bash

find /volume1/openwrt/download -name 'packages.adb' -print0 | while IFS= read -r -d '' adb; do
    dir="$(dirname "$adb")"
    (
      cd $dir
      pwd
      if [ -f "index.json" ];then
        /root/.python3/bin/python3 -c 'import json,glob; packages=[f"{k}-{v}.apk" for k,v in json.load(open("index.json"))["packages"].items()]; [print(f) for f in sorted(glob.glob("*.apk")) if f not in packages]' | xargs -r rm -fv
      fi
    )
done