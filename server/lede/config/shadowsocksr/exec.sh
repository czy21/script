# /bin/bash

function prune() {
  # prune domain
  for i in $(seq $(uci show {{ param_role_name }} | grep '^{{ param_role_name }}\(.*\)=servers' | wc -l) -1 1);do uci del {{ param_role_name }}.@servers[$(($i-1))]; done
}

function backup() {
  echo backup
}