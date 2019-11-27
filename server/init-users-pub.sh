#!/bin/bash

set -e

for file in $(ls ./pubs/*.pub);
    do 
    tunnel_pubs="$tunnel_pubs"command=\"read\",no-X11-forwarding,no-agent-forwarding,no-pty,no-user-rc" `cat $file`\n"
    erp_pubs="$erp_pubs`cat $file`\n"
done
echo -e $tunnel_pubs > tunnel_temp
echo -e $erp_pubs > erp_temp
./user-tunnel.sh $1 -create < tunnel_temp
./user-erp.sh $1 -create < erp_temp
rm -rf tunnel_temp erp_temp
