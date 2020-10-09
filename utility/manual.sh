# docker

# mysql

mysql --host=localhost --port=3306 --user=root --password=sasa -e "drop database if exists erp; create database if not exists erp default charset utf8 collate utf8_general_ci;" && mysqldump erp_bak --host=localhost --port=3306 --user=root --password=sasa | mysql --database=erp --host=localhost --port=3306 --user=root --password=sasa

mysql --database=erp --host=localhost --port=3306 --user=root --password=sasa -e "update release_config set config_value='110' where config_key='Version';update release_config set config_value=Now() where config_key='BuildDate'"

# neo4j-etl
neo4j-etl generate-metadata-mapping --rdbms:url "jdbc:mysql://192.168.2.4:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password Czy.190815 --rdbms:schema cy_db --exclusion-mode-tables include --tables -g .*\.ent_.* --output-mapping-file /d/mysql_cy_db_mapping.json --debug

neo4j-etl export --rdbms:url "jdbc:mysql://192.168.2.4:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password Czy.190815 --neo4j:url "bolt://127.0.0.1:7687" --neo4j:user neo4j --neo4j:password Czy.190815 --using cypher:batch --unwind-batch-size 1000 --tx-batch-size 10000 --mapping-file /d/mysql_cy_db_mapping.json --csv-directory /d/Temp --debug

jenkins_home_des=$(echo $WORKSPACE | awk -F "/workspace" '{print $1}') &&
jenkins_home_source=$(sudo docker inspect --format '{{range $t :=.Mounts}}{{if eq $t.Destination "'${jenkins_home_des}'"}}{{$t.Source}}{{end}}{{end}}' jenkins) &&
HOME=$(echo ${WORKSPACE/${jenkins_home_des}/${jenkins_home_source}})



jenkins_home_des=$(echo $WORKSPACE | awk -F "/workspace" '{print $1}') &&
jenkins_home_source=$(sudo docker inspect --format '{{range $t :=.Mounts}}{{if eq $t.Destination "'${jenkins_home_des}'"}}{{$t.Source}}{{end}}{{end}}' jenkins) &&
HOME=$(echo ${WORKSPACE/${jenkins_home_des}/${jenkins_home_source}})&& mkdir $HOME &&
sudo docker build --file $HOME/script/Dockerfile -t my-python-app .&& sudo docker run -it --rm --name my-running-script -v "$HOME":/usr/src/myapp python:3 python --version