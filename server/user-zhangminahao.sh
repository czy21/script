#!/bin/bash

set -e
# $1: user@host
# example: ./user-zhangpinghao.sh user@host < ~/.ssh/[user]-rsa.pub
ssh $1 "sudo useradd -m zhangpinghao;
        sudo usermod -aG wheel zhangpinghao;
        sudo passwd -d zhangpinghao;
        sudo -u zhangpinghao bash -c "\""set -e;cd;
        mkdir .ssh;chmod 700 .ssh;
        cat >> .ssh/authorized_keys;
        chmod 644 .ssh/authorized_keys;"\"