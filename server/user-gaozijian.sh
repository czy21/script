#!/bin/bash

set -e
# $1: user@host
# example: ./user-gaozijian.sh user@host < ~/.ssh/[user]-rsa.pub
ssh $1 "sudo useradd -m gaozijian;
        sudo usermod -aG wheel gaozijian;
        sudo passwd -d gaozijian;
        sudo -u gaozijian bash -c "\""set -e;cd;
        mkdir .ssh;chmod 700 .ssh;
        cat >> .ssh/authorized_keys;
        chmod 644 .ssh/authorized_keys;"\"