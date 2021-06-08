# docker

# mysql

mysql --host=localhost --port=3306 --user=root --password=sasa -e "drop database if exists erp; create database if not exists erp default charset utf8 collate utf8_general_ci;" && mysqldump erp_bak --host=localhost --port=3306 --user=root --password=sasa | mysql --database=erp --host=localhost --port=3306 --user=root --password=sasa

mysql --database=erp --host=localhost --port=3306 --user=root --password=sasa -e "update release_config set config_value='110' where config_key='Version';update release_config set config_value=Now() where config_key='BuildDate'"

# neo4j-etl
neo4j-etl generate-metadata-mapping --rdbms:url "jdbc:mysql://192.168.2.11:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password Czy.190815 --rdbms:schema cy_db --exclusion-mode-tables include --tables -g .*\.ent_.* --output-mapping-file /d/mysql_cy_db_mapping.json --debug

neo4j-etl export --rdbms:url "jdbc:mysql://192.168.2.11:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password Czy.190815 --neo4j:url "bolt://127.0.0.1:7687" --neo4j:user neo4j --neo4j:password Czy.190815 --using cypher:batch --unwind-batch-size 1000 --tx-batch-size 10000 --mapping-file /d/mysql_cy_db_mapping.json --csv-directory /d/Temp --debug

HOME=$WORKSPACE && pip3 install -r ./erp/script/requirements.txt && cd ./erp/shell/play && python3 build_api_image.py --param param_api_image_tag=1.0.0 && cd $HOME


docker rm -f $(docker ps --filter ancestor=erp:play -q)

docker rmi erp:play

docker ps --filter ancestor=erp:play -q | xargs docker rm

scp -r ubun_a:/home/bruce/lede/bin/targets/ .

# get join cluster command
kubeadm token create --print-join-command

export KUBECONFIG=/etc/kubernetes/admin.conf

kubectl -n kubernetes-dashboard get secret $(kubectl -n kubernetes-dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"

nmcli dev wifi connect XXXX password ****

mount -t nfs 192.168.1.3:/nfs_test /mnt/test1