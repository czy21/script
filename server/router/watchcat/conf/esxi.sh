#!/bin/bash

esxi_host_cmd="ssh esxi"

function close_vms(){
    for t in $1;do
        if `$esxi_host_cmd vim-cmd vmsvc/power.getstate $t | grep 'Powered on' -q`;then
            vm_name=`$esxi_host_cmd vim-cmd vmsvc/get.summary $t | grep name`
            if `$esxi_host_cmd vim-cmd vmsvc/get.summary $t | grep 'toolsOk' -q`;then
              logger -p daemon.info -t "watchcat[$$]" "id: $t $vm_name power.shutdown"
              $esxi_host_cmd vim-cmd vmsvc/power.shutdown $t
            else
              logger -p daemon.info -t "watchcat[$$]" "id: $t $vm_name power.off"
              $esxi_host_cmd vim-cmd vmsvc/power.off $t
            fi
        fi
    done
}

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

# close node
vm_ids=`$esxi_host_cmd vim-cmd vmsvc/getallvms | awk 'NR!=1 {if ($2 ~ "^node") print $1}' | xargs`
close_vms "$vm_ids"
check_vms "$vm_ids"

# close other
vm_ids=`$esxi_host_cmd vim-cmd vmsvc/getallvms | awk 'NR!=1 {if ($2 != "win" && $2 !~ "^node") print $1}' | xargs`
close_vms "$vm_ids"
check_vms "$vm_ids"

# close win
vm_ids=`$esxi_host_cmd vim-cmd vmsvc/getallvms | awk 'NR!=1 {if ($2 == "win") print $1}' | xargs`
close_vms "$vm_ids"
