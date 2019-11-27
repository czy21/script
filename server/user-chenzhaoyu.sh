#!/bin/bash

set -e
# $1: user@host
# example: ./user-chenzhaoyu.sh user@host < ~/.ssh/[user]-rsa.pub
ssh $1 "sudo useradd -m chenzhaoyu;
        sudo usermod -aG wheel chenzhaoyu;
        sudo passwd -d chenzhaoyu;
        sudo -u chenzhaoyu bash -c "\""set -e;cd;
        mkdir .ssh;chmod 700 .ssh;
        cat >> .ssh/authorized_keys;
        chmod 644 .ssh/authorized_keys;"\"