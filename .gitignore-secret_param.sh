#!/bin/bash

param_sed_args="sed "
function remove_secret_param() {
    secret_value=${2:-"<secret_value>"}
    param_sed_args+=" -e \"s|^\($1:\)\(.*\)|\1 $secret_value|\""
}

remove_secret_param 'param_manage_password'
remove_secret_param 'param_db_password'

remove_secret_param 'param_mail_smtp_password'
remove_secret_param 'param_user_ops_ssh_public_key'

remove_secret_param 'param_vaultwarden_admin_token'
remove_secret_param 'param_vsphere_uri' 'user:password@host'

param_sed_args+=" $1"
echo $param_sed_args > .gitignore-secret_param.log
eval $param_sed_args