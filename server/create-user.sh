#!/bin/bash

# sh create-user.sh -h [user@host] -u [username] -i [identity_path]
# -i ./pubs/ | ./pubs/czy-rsa.pub
# -a is_append to authorized_keys for exist user
set -e

host=
username=
public_key=
is_append=0

while [[ $# -ge 1 ]]; do
  case $1 in
  -h)
    host=$2
    shift 2
    ;;
  -u)
    username=$2
    shift 2
    ;;
  -i)
    if test -d $2; then
      for f in $(ls ./pubs/*.pub); do
        public_key="$public_key$(cat $f)\n"
      done
    fi
    if test -f $2; then
      public_key=$(cat $2)
    fi
    shift 2
    ;;
  -a)
    is_append=1
    shift 1
    ;;
  *)
    echo -e "\033[31m$1 un_know input param \033[0m"
    break
    ;;
  esac
done

echo "host -> $host"
echo "username -> $username"
echo "is_append -> $is_append"

if [ $is_append = 1 ]; then
  ssh $host "sudo -u '$username' bash -c "\""set -e;cd;echo -e '$public_key' >> .ssh/authorized_keys;"\"
  exit
fi

ssh $host "sudo useradd -m '$username';
           sudo usermod -aG wheel '$username';
           sudo passwd -d '$username';
           sudo -u '$username' bash -c "\""set -e;cd;mkdir .ssh;chmod 700 .ssh;echo -e '$public_key' >> .ssh/authorized_keys;chmod 644 .ssh/authorized_keys;"\"
