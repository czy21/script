#!/bin/bash

set -e
# $1: user@host
# $2: ~/.ssh/[private_key]
# example: ./init.sh user@host ~/.ssh/[private_key]

# ssh tunnel config
scp $2 $1:
scp -r ./init.d/* $1:/etc/init.d/
ssh $1 "ash -c" \''chmod 600 /root/softium-bruce'\'
ssh $1 "ash -c" \''/etc/init.d/ssh-socks5 enable;'\'

# redsocks config
#scp ./redsocks/redsocks.conf $1:/etc/
#ssh $1 "ash -c" \''/etc/init.d/redsocks enable;'\'

# reboot
#ssh $1 "ash -c" \''reboot;'\'