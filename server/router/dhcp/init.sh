#!/bin/bash

uci show {{ param_role_name }} | grep '^{{ param_role_name }}.@domain\(.*\)=domain' | sed -e 's|^{{ param_role_name }}.@domain|delete \0|g' -e 's|=domain||g' -e '1!G;h;$!d' | uci batch

sed -e '$i commit {{ param_role_name }}' {{ param_role_path }}/{{ param_script_uci_file_name }} | uci batch