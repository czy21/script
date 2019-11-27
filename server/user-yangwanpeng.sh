#!/bin/bash

set -e
# $1: user@host
# example: ./user-yangwanpeng.sh user@host < ~/.ssh/[user]-rsa.pub
ssh $1 "sudo useradd -m yangwanpeng;
        sudo usermod -aG wheel yangwanpeng;
        sudo passwd -d yangwanpeng;
        sudo -u yangwanpeng bash -c "\""set -e;cd;
        mkdir .ssh;chmod 700 .ssh;
        cat >> .ssh/authorized_keys;
        chmod 644 .ssh/authorized_keys;"\"