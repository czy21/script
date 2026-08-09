#!/bin/bash

set -e

function apply_device_patch(){
  patch_dir=$1
  git restore -SW $patch_dir; git clean -fd $patch_dir
  (cd /ci;rsync -avmR --exclude='*.device.patch' $patch_dir /builder)

  find $patch_dir -type f -name '*.rej' -delete
  find /ci/$patch_dir -type f -name '*.device.patch' -print0 | sort -z | xargs -I % -t -0 -n 1 sh -c "patch -d './' --no-backup-if-mismatch -p1 -F 1 -i '%'"
  find $patch_dir -type f -name '*.rej' -delete
}

show_help() {
    cat <<EOF
Usage:
  $0 <target> [options]

Target:
  mediatek/filogic        OpenWrt target/subtarget

Options:
  --init                  Initialize build environment
  --diff                  Show diff
  --update                Update source/config
  --deploy                Deploy artifact
  --reset                 Reset source/config
  --patch                 Apply patch
  --prebuilt              Prepare prebuilt
  --build                 Build image
  -h, --help              Show this help message

Examples:
  $0 mediatek/filogic --init
  $0 mediatek/filogic --update --patch --build
EOF
}

# no args
if [[ $# -eq 0 ]]; then
    show_help
    exit 1
fi

target=$1
shift 1

IFS='/' read -r target subtarget <<< $target

echo "===== $target $subtarget ====="

init=false
diff=false
update=false
deploy=false
reset=false
patch=false
prebuilt=false
build=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --init)
            init=true
            shift
            ;;
        --diff)
            diff=true
            shift
            ;;
        --update)
            update=true
            shift
            ;;
        --deploy)
            deploy=true
            shift
            ;;
        --reset)
            reset=true
            shift
            ;;
        --patch)
            patch=true
            shift
            ;;
        --prebuilt)
            prebuilt=true
            shift
            ;;
        --build)
            build=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo
            show_help
            exit 1
            ;;
    esac
done

if [ "$diff" = true ];then
  exclude_rules=(
    ':(exclude).gitignore'
    ':(exclude)feeds.conf.default*'
    ':(exclude)package/base-files/Makefile'
  )
  git diff --name-status -- . "${exclude_rules[@]}"
  git diff -- . "${exclude_rules[@]}" | sed -e '/^diff --git/d' -e 's|^index .*||' > /ci/diff.patch
  exit 0
fi

if [ $reset = true ];then
  git reset --hard HEAD;git clean -f
  exit 0
fi

if [ "$init" = true ];then
  find . -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  
  git init
  git remote add origin $origin/openwrt/openwrt.git
  git fetch --tags origin
  if [ "$branch" = "master" ] || [ "$branch" = "main" ]; then
      git checkout -B "$branch" "origin/$branch"
  else
      git checkout -B "$branch" "$(git tag --sort=-version:refname -l "v${branch#openwrt-}*" | head -n1)"
  fi
  echo '/openwrt-toolchain*' >> .gitignore
fi

[ -f "feeds.conf.default" ] || {
  echo "feeds.conf.default not found"
  exit 0
}

ln -snf /data/apk.key private-key.pem
ln -snf /data/pri.key key-build

mirror=${mirror:-https://openwrt-dlc.czy21.com/openwrt}
version=$(git describe --tags --exact-match 2>/dev/null | sed 's/^v//')
version_path=snapshots

# https://s3-ccache.openwrt-ci.ansuel.com
ccache_from=https://openwrt-dlc.czy21.com/openwrt-ccache
ccache_type=kernel

[ -n "$version" ] && version_path=releases/$version

download_release_dir=/data/download/$version_path

echo '===== Prepare prebuilt tools ====='
mkdir -p staging_dir build_dir

rm -rf staging_dir/host build_dir/host
ln -snf /prebuilt_tools/staging_dir/host staging_dir/host
ln -snf /prebuilt_tools/build_dir/host build_dir/host

./scripts/ext-tools.sh --refresh

ls -al staging_dir build_dir

[ -f "feeds.conf.default.bak" ] || cp -rv feeds.conf.default feeds.conf.default.bak
sed -e "s|https://git.openwrt.org/\(.*\)/|$origin/openwrt/|g" \
    -e "s|https://github.com/openwrt/|$origin/openwrt/|g" feeds.conf.default.bak > feeds.conf.default

if [ "$update" = true ];then
  ./scripts/feeds update -a
  ./scripts/feeds install -a
fi

> .config
cat >> .config << EOF
CONFIG_TARGET_${target}=y
CONFIG_TARGET_${target}_${subtarget}=y
CONFIG_TARGET_MULTI_PROFILE=y
EOF

[ -f /ci/.config ] && eval "printf '%s\n' \"$(< /ci/.config)\"" >> .config

grep -q '^CONFIG_TARGET_DEVICE_' .config || {
  echo 'CONFIG_TARGET_DEVICE_ not found in'
  exit 0
}

cat >> .config << EOF
CONFIG_ALL_KMODS=y
CONFIG_TARGET_PER_DEVICE_ROOTFS=y
CONFIG_DEVEL=y
CONFIG_AUTOREMOVE=y
CONFIG_LOCALMIRROR="https://openwrt-dlc.czy21.com/openwrt-sources"
# CONFIG_KERNEL_KALLSYMS is not set
CONFIG_IMAGEOPT=y
EOF

cat >> .config << EOF
CONFIG_PACKAGE_luci=y
CONFIG_PACKAGE_luci-ssl=y
CONFIG_PACKAGE_luci-app-attendedsysupgrade=y
EOF

if [ "$patch" = true ];then
  echo '===== Patch ====='

  apply_device_patch package/
  apply_device_patch target/linux/
fi

SUMS_FILE="$mirror/${version_path}/targets/${target}/${subtarget}/sha256sums"
echo "SUMS_FILE: $SUMS_FILE"

echo '===== Download external toolchain/sdk ====='
TOOLCHAIN_STRING="$( curl ${SUMS_FILE} | grep -P ".*openwrt-toolchain.*tar.(xz|zst)")"
TOOLCHAIN_FILE=$(echo "$TOOLCHAIN_STRING" | sed -n -E -e 's/.*(openwrt-toolchain.*.tar.(xz|zst))$/\1/p')
TOOLCHAIN_NAME=$(echo $TOOLCHAIN_FILE | sed -E -e 's/.tar.(xz|zst)$//')
[ -d "${TOOLCHAIN_NAME}" ] || (wget -nv -O - $mirror/${version_path}/targets/${target}/${subtarget}/${TOOLCHAIN_FILE} | tar --zstd -xf -)

echo '===== Download and extract prebuilt llvm ====='
LLVM_STRING="$( curl ${SUMS_FILE} | grep -P ".*llvm-bpf.*tar.(xz|zst)")"
LLVM_FILE=$(echo "$LLVM_STRING" | sed -n -E -e 's/.*(llvm-bpf.*.tar.(xz|zst))$/\1/p')
LLVM_NAME=$(echo $LLVM_FILE | sed -E -e 's/.tar.(xz|zst)$//')
[ -d "${LLVM_NAME}" ] || (wget -nv -O - $mirror/${version_path}/targets/${target}/${subtarget}/${LLVM_FILE} | tar --zstd -xf -)

echo '===== Download and extract ccache cache from s3 ====='
ccache_name=ccache-${ccache_type}-${target}-${subtarget}$([ -n "$version" ] && echo "-$branch")
CCACHE_DIR=$(pwd)/.ccache
CCACHE_CONFIGPATH2=$(pwd)/staging_dir/host/etc/ccache.conf
[ -d "$CCACHE_DIR" ] || (wget -nv -O - $ccache_from/${ccache_name}.tar | tar -xf -)

echo '===== Configure ccache and apply fixes ====='
> $CCACHE_CONFIGPATH2

echo compiler_type=gcc >> $CCACHE_CONFIGPATH2
[ kernel = 'kernel' ] && echo max_size=1G >> $CCACHE_CONFIGPATH2
[ kernel = 'packages' ] && echo max_size=8G >> $CCACHE_CONFIGPATH2

echo depend_mode=true >> $CCACHE_CONFIGPATH2
echo sloppiness=file_macro,locale,time_macros,include_file_ctime,include_file_mtime >> $CCACHE_CONFIGPATH2

echo CONFIG_CCACHE=y >> .config

echo '===== Reset ccache stats ====='
staging_dir/host/bin/ccache --zero-stats

echo '===== Configure external toolchain ====='
./scripts/ext-toolchain.sh \
  --toolchain ${TOOLCHAIN_NAME}/toolchain-* \
  --overwrite-config \
  --config ${target}/${subtarget}

echo '===== Configure prebuilt llvm ====='
echo CONFIG_USE_LLVM_PREBUILT=y >> .config

./scripts/diffconfig.sh > /ci/diff.config

if [ "$build" = true ];then
  make CONFIG_BUILDBOT=y prepare -j$(nproc) BUILD_LOG=1
  make CONFIG_BUILDBOT=y package/{compile,install}  -j$(nproc) BUILD_LOG=1
  make CONFIG_BUILDBOT=y target/imagebuilder/install -j$(nproc) BUILD_LOG=1
fi

if [ "$deploy" = true ];then

  echo '===== Deploy ====='
  (
    cd bin
    rsync -avmR \
      --include='*/' \
      --include='kernel-debug.tar.zst' \
      --include='*.buildinfo' \
      --include="*${target}-${subtarget}*" \
      --exclude="*" \
      targets/${target}/${subtarget} ${download_release_dir}
  )
  make -j6 BIN_DIR=${download_release_dir}/targets/${target}/${subtarget} checksum V=s
fi