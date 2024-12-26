#!/bin/bash

esxi_host_cmd="ssh esxi"
esxi_hostname=`$esxi_host_cmd -G | sed -n 's/^hostname \(.*\)/\1/p'`

function check_vms(){
    vms_off=false
    while [ $vms_off == false ]
    do
      vms_off=true
      for t in $1;do
        if `$esxi_host_cmd vim-cmd vmsvc/power.getstate $t | grep 'Powered on' -q`;then
          vms_off=false
          break
        fi
      done
      [ $vms_off == false ] && sleep 10s
    done
}

function close_vms(){
    for t in $1;do
        if `$esxi_host_cmd vim-cmd vmsvc/power.getstate $t | grep 'Powered on' -q`;then
            vm_name=`$esxi_host_cmd vim-cmd vmsvc/get.summary $t | grep 'name' | sed -e 's/[[:blank:]]//g' -e 's/,//g' -e 's/"//g'`
            if `$esxi_host_cmd vim-cmd vmsvc/get.summary $t | grep 'toolsOk' -q`;then
              logger -p daemon.info -t "watchcat[$$]" "id=$t $vm_name power.shutdown"
              $esxi_host_cmd vim-cmd vmsvc/power.shutdown $t
            else
              logger -p daemon.info -t "watchcat[$$]" "id=$t $vm_name power.off"
              $esxi_host_cmd vim-cmd vmsvc/power.off $t
            fi
        fi
    done
    check_vms $@
}

# close node
vm_ids=`$esxi_host_cmd vim-cmd vmsvc/getallvms | awk 'NR!=1 {if ($2 ~ "^node") print $1}' | xargs`
close_vms "$vm_ids"

# close other
vm_ids=`$esxi_host_cmd vim-cmd vmsvc/getallvms | awk 'NR!=1 {if ($2 != "win" && $2 !~ "^node") print $1}' | xargs`
close_vms "$vm_ids"

# close win
vm_ids=`$esxi_host_cmd vim-cmd vmsvc/getallvms | awk 'NR!=1 {if ($2 == "win") print $1}' | xargs`
close_vms "$vm_ids"

# notify
user_mail=`sed -n 's/^user \(.*\)/\1/p' /etc/msmtprc`
echo -e "Subject: Watchcat `basename $BASH_SOURCE`\n\nHostName: $esxi_hostname vms closed" | msmtp $user_mail