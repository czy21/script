# Initial
```shell
# start service: /usr/sbin/slapd -h "ldap:/// ldapi:///"
# show config
ldapsearch -Y EXTERNAL -H ldapi:/// -b olcDatabase={1}mdb,cn=config
# convert slapd.conf(5) to slapd.d
slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
# set access
sed -i 's|^olcAccess.*|olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth manage by * break|g' '/etc/openldap/slapd.d/cn=config/olcDatabase={0}config.ldif'
# import schema
find /etc/openldap/schema/ -regex '.*\(cosine\|nis\|inetorgperson\|log\).ldif' -exec ldapadd -Y EXTERNAL -H ldapi:/// -f {} \;
```

# Backup and Restore
```shell
# backup
nice /usr/sbin/slapcat -b cn=config > config.ldif
nice /usr/sbin/slapcat -b dc=example,dc=com > example.com.ldif
# restore
slapadd -F /etc/ldap/slapd.d -b cn=config -l config.ldif
slapadd -F /etc/ldap/slapd.d -b dc=example,dc=com -l example.com.ldif
```