#!/bin/bash

esxi_host_cmd="ssh esxi"
esxi_hostname=`$esxi_host_cmd -G | sed -n 's/^hostname \(.*\)/\1/p'`

$esxi_host_cmd "/sbin/shutdown.sh && /sbin/poweroff"

# notify
user_mail=`sed -n 's/^user \(.*\)/\1/p' /etc/msmtprc`
echo -e "Subject: Watchcat `basename $BASH_SOURCE`\n\nHostName: $esxi_hostname host closed" | msmtp $user_mail