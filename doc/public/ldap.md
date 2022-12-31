# Initial
```shell
# start service: /usr/sbin/slapd -h "ldap:/// ldapi:///"
# show config
ldapsearch -Y EXTERNAL -H ldapi:/// -b olcDatabase={1}mdb,cn=config
```
# Backup and Restore
```shell
# restore
slapadd -F /etc/ldap/slapd.d -b cn=config -l config.ldif
slapadd -F /etc/ldap/slapd.d -b dc=example,dc=com -l example.com.ldif
```