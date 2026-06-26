#!/bin/bash

cd $(cd "$(dirname "$0")"; pwd)

path=$1

find ${path} -type d -name node_modules -prune -o -type f -path '*/.github/workflows/*.yml' -print0 | while IFS= read -r -d '' t; do
  grep -Eo 'uses:\s*[^ ]+' "$t" | awk '{
      split($2, arr, "@"); 
      print $2, "https://github.com/" arr[1]
  }'
done | sort | uniq

read -a sed_args <<< $(xargs -n 2 bash -c 'printf -- "-e s|${0}@.*|${0}@${1}| "' << 'EOF'
actions/checkout v7
EOF
)

find "${path}" -type d -name node_modules -prune -o -type f -path '*/.github/workflows/*.yml' -print0 | while IFS= read -r -d '' t; do
  set -x
  sed -i "${sed_args[@]}" "$t"
  { set +x; } 2>/dev/null
done