#!/bin/bash

set -e
# $1: user@host
# $2: -create | -import
# -init ./user-tunnel.sh user@host -create
# -import ./user-tunnel.sh user@host -import < ~/.ssh/[user]-rsa.pub
case "$2" in
        -create)
        ssh $1 "sudo useradd -m tunnel;
                sudo -u tunnel bash -c "\""set -e;cd;
                mkdir .ssh;chmod 700 .ssh;
                cat >> .ssh/authorized_keys;
                chmod 644 .ssh/authorized_keys;"\" 
        ;;
        -import)
        ssh $1 "sudo -u tunnel bash -c" \''set -e;cd;
                echo -n "command=\"read\",no-X11-forwarding,no-agent-forwarding,no-pty,no-user-rc " >>.ssh/authorized_keys;
                cat >>.ssh/authorized_keys;'\'
        ;;
        *)
        echo -e "\033[40;33m unknow input param \033[0m"
        ;;
esac