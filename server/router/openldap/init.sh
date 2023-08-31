#!/bin/bash

param_command="{{ param_command }}"
ldap_etc_path="{{ param_ldap_etc_path }}"
config_ldif_file="{{ param_role_output_path }}/conf/config.ldif"
domain_ldif_file="{{ param_role_output_path }}/conf/domain.ldif"
config_ldif_bak_file="{{ param_role_bak_path }}/config.ldif"
domain_ldif_bak_file="{{ param_role_bak_path }}/domain.ldif"
config_ldif_etc_file="${ldap_etc_path}/slapd.d/cn=config/olcDatabase={0}config.ldif"
mdb_ldif_etc_file="${ldap_etc_path}/slapd.d/cn=config/olcDatabase={1}mdb.ldif"
mkdir -p {{ param_ldap_data }}/ ${ldap_etc_path}/slapd.d/
if [ "install" == "${param_command}" ];then
  if [ ! -f "${config_ldif_etc_file}" ]; then
      slaptest -f ${ldap_etc_path}/slapd.conf -F ${ldap_etc_path}/slapd.d
  fi
  sed -i 's|^olcAccess.*|olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth manage by * none|g' ${config_ldif_etc_file}
  sed -i 's|^olcDbDirectory.*|olcDbDirectory: {{ param_ldap_data }}|g' ${mdb_ldif_etc_file}
  /etc/init.d/openldap restart
  ldapadd -Y EXTERNAL -H ldapi:/// -f ${config_ldif_file}
  ldapadd -x -D cn=admin,dc="{{ param_ldap_domain }}",dc=com -W -f ${domain_ldif_file}
  find ${ldap_etc_path}/schema/ -regex '.*\(cosine\|nis\|inetorgperson\|log\).ldif' -exec ldapadd -Y EXTERNAL -H ldapi:/// -f {} \;
fi

if [ "backup" == "${param_command}" ];then
  nice /usr/sbin/slapcat -b cn=config > ${config_ldif_bak_file}
  nice /usr/sbin/slapcat -b dc="{{ param_ldap_domain }}",dc=com > ${domain_ldif_bak_file}
fi

if [ "restore" == "${param_command}" ];then
  /etc/init.d/openldap stop
  sed -i -e 's|^\s*mkdir|#\0|' -e 's|"ldap://localhost/.*"|"ldap:/// ldaps:/// ldapi:///"|' /etc/init.d/openldap
  rm -rf {{ param_ldap_data }}/* ${ldap_etc_path}/slapd.d/*
  slapadd -F ${ldap_etc_path}/slapd.d -b cn=config -l ${config_ldif_bak_file}
  slapadd -F ${ldap_etc_path}/slapd.d -b dc="{{ param_ldap_domain }}",dc=com -l ${domain_ldif_bak_file}
  /etc/init.d/openldap start
fi