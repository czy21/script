#!/bin/bash
# sh override_config.sh user@host

host=$1
ssh $host 'rm -rf $HOME/lede/files/ && mkdir -p $HOME/lede/files/'
scp -r ./etc $host:'$HOME/lede/files/'