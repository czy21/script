
params=("param_mail_smtp_password" "param_vaultwarden_admin_token")
param_sed_args="sed "
for t in ${params[@]};do
  param_sed_args+=" -e \"s|^\($t:\)\(.*\)|\1|\""
done
param_sed_args+=" $1"
echo $param_sed_args > .gitignore-secret_param.log
eval $param_sed_args