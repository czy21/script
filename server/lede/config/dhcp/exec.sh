# /bin/bash

function prune() {
  # prune domain
  for i in $(uci show dhcp | grep '^dhcp.@domain\(.*\)=domain' | sed "s/=domain//; s/[^[:digit:]]//g" | sort -rn); do uci del dhcp.@domain[${i}];done
}

function backup() {

}