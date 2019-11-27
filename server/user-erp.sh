#!/bin/bash

# $1: user@host
# $2: -create | -import
# -init ./user-tunnel.sh user@host -create
# -import ./user-tunnel.sh user@host -import < ~/.ssh/[user]-rsa.pub
set -e
case "$2" in
        -create)
        ssh $1 "sudo useradd -m erp;
                sudo passwd -d erp;
                sudo -u erp bash -c "\""set -e;cd;
                chmod 755 ~;mkdir .ssh;chmod 700 .ssh;
                cat >> .ssh/authorized_keys;
                chmod 644 .ssh/authorized_keys;
                mkdir api web"\"
        ;;
        -import)
        ssh $1 "sudo -u erp bash -c" \''set -e;cd;cat >>.ssh/authorized_keys;'\'
        ;;
        *)
        echo -e "\033[40;33m unknow input param \033[0m"
        ;;
esac