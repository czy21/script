
sed -e "s|^\(param_mail_smtp_password:\)\(.*\)|\1|" \
    -e "s|^\(param_vaultwarden_admin_token:\)\(.*\)|\1|" $1