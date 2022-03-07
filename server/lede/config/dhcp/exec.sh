# /bin/bash

function prune() {
  # prune
  for i in $(seq $(uci show {{ param_role_name }} | grep '^{{ param_role_name }}\(.*\)=domain' | wc -l) -1 1);do uci del {{ param_role_name }}.@domain[$(($i-1))]; done
}