#!/bin/bash

LOG_TAG="watchcat.esxi"

esxi_host_cmd="ssh esxi"

function close_vms(){
    for t in $1;do
        if [ `$esxi_host_cmd vim-cmd vmsvc/power.getstate $t | grep 'Powered on' -q && echo true` ];then
            vm_name=`$esxi_host_cmd vim-cmd vmsvc/get.summary $t | grep name`
            if [ `$esxi_host_cmd vim-cmd vmsvc/get.summary $t | grep toolsOk -q && echo true` ];then
              logger -t "${LOG_TAG}" "id: $t $vm_name power.shutdown"
              $esxi_host_cmd vim-cmd vmsvc/power.shutdown $t
            else
              logger -t "${LOG_TAG}" "id: $t $vm_name power.off"
              $esxi_host_cmd vim-cmd vmsvc/power.off $t
            fi
        fi
    done
}

function check_vms(){
    vms_off=false
    while [ $vms_off == false ]
    do
      for t in $1;do
        vms_off=`$esxi_host_cmd vim-cmd vmsvc/power.getstate $t | grep 'Powered off' -q && echo true || false`
      done
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
