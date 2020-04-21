#!/bin/bash

set -e
# $1: user@host
# example: ./user-jiangjiatao.sh user@host < ~/.ssh/[user]-rsa.pub
ssh $1 "sudo useradd -m jiangjiatao;
        sudo usermod -aG wheel jiangjiatao;
        sudo passwd -d jiangjiatao;
        sudo -u jiangjiatao bash -c "\""set -e;cd;
        mkdir .ssh;chmod 700 .ssh;
        cat >> .ssh/authorized_keys;
        chmod 644 .ssh/authorized_keys;"\"