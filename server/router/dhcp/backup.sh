#!/bin/bash


bak_path={{ param_role_path }}/___temp/bak
mkdir -p ${bak_path}

cat /dev/null > ${bak_path}/{{ param_script_uci_file_name }}

uci show {{ param_role_name }} \
| grep '^{{ param_role_name }}.@domain' \
| sed \
-e 's|^{{ param_role_name }}.@domain\[\(.*\)\]|set {{ param_role_name }}.@domain[-1]\2|g' \
-e 's|set {{ param_role_name }}.@domain\[-1\]=domain|add {{ param_role_name }} domain|g' >> ${bak_path}/{{ param_script_uci_file_name }}