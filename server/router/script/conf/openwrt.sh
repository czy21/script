#!/bin/bash

openwrt_download=/volume1/openwrt/download
immortalwrt_download=/volume1/openwrt/download/immortalwrt

find ${openwrt_download} -name 'packages.adb' -print0 | while IFS= read -r -d '' t; do
    dir="$(dirname "$t")"
    (
      cd $dir
      if [ -f "index.json" ];then
        /root/.python3/bin/python3 -c 'import sys,json,pathlib; packages=[f"{k}-{v}.apk" for k,v in json.load(open("index.json"))["packages"].items()]; [print(f) for f in sorted(pathlib.Path(sys.argv[1]).rglob("*.apk")) if f.name not in packages]' ${dir} | xargs -r rm -fv
      fi
    )
done

function prune_download_source() {
  source_dir=$1
  find ${openwrt_download}/releases ${openwrt_download}/snapshots -name 'plugin' -type d -print0 | while IFS= read -r -d '' t; do
    dir=$t
    parent_dir="$(dirname "$t")"
    src=$source_dir/${parent_dir#$openwrt_download/}
    (
      cd $dir
      if [ -f "index.json" ];then
        /root/.python3/bin/python3 -c 'import sys,json,pathlib; packages=[f"{k}-{v}.apk" for k,v in json.load(open("index.json"))["packages"].items()]; [print(f) for f in sorted(pathlib.Path(sys.argv[1]).rglob("*.apk")) if f.name not in packages]' ${src} | xargs -r rm -fv
      fi
    )
  done
}

prune_download_source $immortalwrt_download