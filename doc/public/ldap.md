# Initial
```shell
# start service: /usr/sbin/slapd -h "ldap:/// ldapi:///"
# show config
ldapsearch -Y EXTERNAL -H ldapi:/// -b olcDatabase={1}mdb,cn=config
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