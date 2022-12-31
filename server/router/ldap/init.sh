#!/bin/bash

param_command="{{ param_command }}"
param_init_config_ldif_file="{{ param_role_output_path }}/conf/config.ldif"
param_init_domain_ldif_file="{{ param_role_output_path }}/conf/domain.ldif"
param_bak_config_ldif_file="{{ param_role_temp_path }}/config.ldif.bak"
param_bak_domain_ldif_file="{{ param_role_temp_path }}/domain.ldif.bak"
param_olc_config_ldif_file='/etc/openldap/slapd.d/cn=config/olcDatabase={0}config.ldif'
if [ "install" == "${param_command}" ];then
  if [ ! -f "${param_olc_config_ldif_file}" ]; then
      mkdir -p /etc/openldap/slapd.d && slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
  fi
  sed -i 's|^olcAccess.*|olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth manage by * none|g' ${param_olc_config_ldif_file}
  ldapadd -Y EXTERNAL -H ldapi:/// -f ${param_init_config_ldif_file}
  ldapadd -x -D cn=admin,dc="{{ param_ldap_domain }}",dc=com -W -f ${param_init_domain_ldif_file}
  find /etc/openldap/schema/ -regex '.*\(cosine\|nis\|inetorgperson\|log\).ldif' -exec ldapadd -Y EXTERNAL -H ldapi:/// -f {} \;
fi

if [ "backup" == "${param_command}" ];then
  nice /usr/sbin/slapcat -b cn=config > ${param_bak_config_ldif_file}
  nice /usr/sbin/slapcat -b dc="{{ param_ldap_domain }}",dc=com > ${param_bak_domain_ldif_file}
fi

if [ "restore" == "${param_command}" ];then
  echo "还原"
fi