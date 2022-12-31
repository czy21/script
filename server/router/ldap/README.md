```shell
# start service: /usr/sbin/slapd -h "ldap:/// ldaps:/// ldapi:///"
# show config
ldapsearch -Y EXTERNAL -H ldapi:/// -b olcDatabase={1}mdb,cn=config
```