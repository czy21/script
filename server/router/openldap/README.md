```shell
# show config
ldapsearch -Y EXTERNAL -H ldapi:/// -b olcDatabase={1}mdb,cn=config
# modify password
slappasswd -s <password> # generate password
```