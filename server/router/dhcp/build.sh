#!/bin/bash

function backup() {
  local bak_path={{ param_role_path }}/___temp/bak
  mkdir -p ${bak_path}

  cat /dev/null > ${bak_path}/{{ param_script_uci_file_name }}

  uci show {{ param_role_name }} \
  | grep '@domain' \
  | sed \
  -e 's|\[.*\]|[-1]|g' \
  -e 's|.*=domain|add {{ param_role_name }} domain|g' >> ${bak_path}/{{ param_script_uci_file_name }}
}

function install() {
	uci show {{ param_role_name }} | grep '^{{ param_role_name }}.@domain\(.*\)=domain' | sed -e 's|^{{ param_role_name }}.@domain|delete \0|g' -e 's|=domain||g' -e '1!G;h;$!d' | uci batch
  sed -e '$i commit {{ param_role_name }}' {{ param_role_path }}/{{ param_script_uci_file_name }} | uci batch
}

$1