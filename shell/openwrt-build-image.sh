#!/bin/bash

env

sed -i -e '/^wget.*sha256sums.asc/d' -e '/^gpg.*/d' -e '/^sha256sum -c.*/d' setup.sh && ./setup.sh

[ -f "Makefile.bak" ] || cp -rv Makefile Makefile.bak
cp -rv Makefile.bak Makefile

package_dir=$(echo "$VERSION_PATH" | awk -F'[/.]' '$1=="releases" {print "releases/""packages-"$2"."$3; next} {print "snapshots/""packages"}')
if grep -q '^CONFIG_USE_APK=y' .config;then
  sed -i -e 's|$(APK) add|\0 --force-overwrite|' Makefile
  cat Makefile

  [ -f "repositories.bak" ] || cp -rv repositories repositories.bak
  cp -rv repositories.bak repositories

  openwrt_plugin=$(sed -n -e 's|\(.*\)base\(\.*\)|\1plugin\2|p' repositories | sed -e "s|https://downloads.openwrt.org/$VERSION_PATH/packages|https://openwrt-download.czy21.com/$package_dir|")
  sed -i -e "1i ${openwrt_plugin}" -e "s|https://downloads.openwrt.org|${mirror}|" repositories
  cat repositories

  cp -rv /data/apk.pub keys/

  mkdir -p files/etc/apk/keys
  cp -rv /data/apk.pub files/etc/apk/keys/openwrt-plugin.pem

  mkdir -p files/etc/uci-defaults/
  tee files/etc/uci-defaults/99-setup << EOF
#!/bin/sh
echo "Appending customfeeds..."
echo "${openwrt_plugin}" > /etc/apk/repositories.d/customfeeds.list
sed -i -e 's|.*disabled.*||' /etc/config/wireless || true
EOF
else
  sed -i -e 's|$(OPKG) install $(BUILD_PACKAGES)|\0 --force-overwrite|' Makefile

  [ -f "repositories.conf.bak" ] || cp -rv repositories.conf repositories.conf.bak
  cp -rv repositories.conf.bak repositories.conf

  openwrt_plugin=$(sed -n -e 's|openwrt_base\(.*\)base$|openwrt_plugin\1plugin|p' repositories.conf | sed -e "s|https://downloads.openwrt.org/$VERSION_PATH/packages|https://openwrt-download.czy21.com/$package_dir|")
  sed -i -e "\$a ${openwrt_plugin}" -e "s|https://downloads.openwrt.org|${mirror}|" repositories.conf
  cat repositories.conf

  ln -snf /data/pri.key key-build
  ln -snf /data/pub.key key-build.pub

  OPKG_KEYS=keys ./scripts/opkg-key add /data/pub.key
  OPKG_KEYS=files/etc/opkg/keys ./scripts/opkg-key add /data/pub.key

  mkdir -p files/etc/uci-defaults/
  tee files/etc/uci-defaults/99-setup << EOF
#!/bin/sh
echo "Appending customfeeds..."
echo "${openwrt_plugin}" > /etc/opkg/customfeeds.conf
if [ -f "/etc/config/wireless" ];then
  sed -i -e 's|.*disabled.*||' /etc/config/wireless
fi
EOF
fi
# make image PROFILE=generic PACKAGES="" ROOTFS_PARTSIZE=1024 CONFIG_VMDK_IMAGES=y CONFIG_ISO_IMAGES=y FILES=files
make image PROFILE=ikuai_q3000-ubi PACKAGES="-dnsmasq kmod-tcp-bbr kmod-nf-tproxy kmod-nf-socket kmod-ipt-ipset dnsmasq-full softethervpn5-server openssh-client luci luci-compat luci-proto-wireguard qrencode luci-app-uhttpd luci-app-nlbwmon luci-app-wol luci-app-vlmcsd luci-app-acme acme-acmesh-dnsapi acme-sync luci-app-ddns ddns-scripts ddns-scripts-aliyun ddns-scripts-cloudflare luci-app-watchcat luci-app-ttyd luci-app-commands"