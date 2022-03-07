
function prune_list_by_types() {
  for t in ${role_config_types}; do
    type_name=${role_name}.@${t}
    type_total=$(uci show ${role_name} | grep '^'${role_name}'\(.*\)='${t}'' | wc -l)
    echo -e "\033[32mprune \033[0m=> ${type_name} total: ${type_total}"
    for i in $(seq ${type_total} -1 1);do
      uci del ${type_name}[$(($i-1))]
    done
  done
}