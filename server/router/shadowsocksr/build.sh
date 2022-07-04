#!/bin/bash

function backup() {
  local bak_path={{ param_role_path }}/___temp/bak
  mkdir -p ${bak_path}

  cat /dev/null > ${bak_path}/{{ param_script_uci_file_name }}

  uci show {{ param_role_name }} \
  | grep '@server_subscribe' \
  | sed \
  -e 's|\[.*\]|[-1]|g' \
  -e 's|.*=server_subscribe|add {{ param_role_name }} server_subscribe|g' >> ${bak_path}/{{ param_script_uci_file_name }}
}

function install() {
	uci show {{ param_role_name }} | grep '.service_name' | sed -e 's|.service_name.*$||g' -e 's|^ddns|delete \0|g' | uci batch
  sed -e '$i commit {{ param_role_name }}' {{ param_role_path }}/{{ param_script_uci_file_name }} | uci batch
}

$1