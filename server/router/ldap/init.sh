#!/bin/bash

param_command="{{ param_command }}"
ldap_etc_path="{{ param_ldap_etc_path }}"
config_ldif_file="{{ param_role_output_path }}/conf/config.ldif"
domain_ldif_file="{{ param_role_output_path }}/conf/domain.ldif"
config_ldif_bak_file="{{ param_role_temp_path }}/config.ldif.bak"
domain_ldif_bak_file="{{ param_role_temp_path }}/domain.ldif.bak"
config_ldif_etc_file="${ldap_etc_path}/slapd.d/cn=config/olcDatabase={0}config.ldif"
if [ "install" == "${param_command}" ];then
  if [ ! -f "${config_ldif_etc_file}" ]; then
      mkdir -p ${ldap_etc_path}/slapd.d && slaptest -f ${ldap_etc_path}/slapd.conf -F ${ldap_etc_path}/slapd.d
  fi
  sed -i 's|^olcAccess.*|olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth manage by * none|g' ${config_ldif_etc_file}
  ldapadd -Y EXTERNAL -H ldapi:/// -f ${config_ldif_file}
  ldapadd -x -D cn=admin,dc="{{ param_ldap_domain }}",dc=com -W -f ${domain_ldif_file}
  find ${ldap_etc_path}/schema/ -regex '.*\(cosine\|nis\|inetorgperson\|log\).ldif' -exec ldapadd -Y EXTERNAL -H ldapi:/// -f {} \;
fi

if [ "backup" == "${param_command}" ];then
  nice /usr/sbin/slapcat -b cn=config > ${config_ldif_bak_file}
  nice /usr/sbin/slapcat -b dc="{{ param_ldap_domain }}",dc=com > ${domain_ldif_bak_file}
fi

if [ "restore" == "${param_command}" ];then
  slapadd -F ${ldap_etc_path}/slapd.d -b cn=config -l ${config_ldif_bak_file}
  slapadd -F ${ldap_etc_path}/slapd.d -b dc="{{ param_ldap_domain }}",dc=com -l ${domain_ldif_bak_file}
fi