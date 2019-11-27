#!/bin/bash

wget --no-check-certificate -O shadowsocks-libev.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-libev.sh
sudo chmod +x shadowsocks-libev.sh
sudo ./shadowsocks-libev.sh 2>&1 | tee shadowsocks-libev.log