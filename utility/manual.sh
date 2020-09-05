# docker
sudo docker run --rm -u gradle -v "$PWD"/code/api/:/home/gradle/project -v "$HOME"/init.gradle:/home/gradle/.gradle/init.gradle -w /home/gradle/project/ gradle:jdk11 gradle clean build -b portal/build.gradle

sudo docker build --tag erp:1.0.0 --file script/domain/template/api/Dockerfile --build-arg jar=code/api/portal/build/libs/portal.jar .

sudo docker run -d -p 8075:8075 --name=erp --net=host czy/erp

sudo docker images | grep erp | awk '{print $3}' | xargs sudo docker rmi

# mysql
mysql --database=erp --host=localhost --port=3306 --user=root --password=sasa -vvv < D:\Developer\JavaProject\erp\_temp\db\all_in_one.sql > local_upgrade_db.py.log

mysql --host=localhost --port=3306 --user=root --password=sasa -e "drop database if exists erp; create database if not exists erp default charset utf8 collate utf8_general_ci;" && mysqldump erp_bak --host=localhost --port=3306 --user=root --password=sasa | mysql --database=erp --host=localhost --port=3306 --user=root --password=sasa

mysql --database=erp --host=localhost --port=3306 --user=root --password=sasa -e "update release_config set config_value='110' where config_key='Version';update release_config set config_value=Now() where config_key='BuildDate'"

# neo4j-etl
neo4j-etl generate-metadata-mapping --rdbms:url "jdbc:mysql://192.168.2.4:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password ***REMOVED*** --rdbms:schema cy_db --exclusion-mode-tables include --tables -g .*\.ent_sfl.* --output-mapping-file /d/mysql_cy_db_mapping.json --debug

neo4j-etl export --rdbms:url "jdbc:mysql://192.168.2.4:3306/cy_db?autoReconnect=true&useSSL=false&useCursorFetch=true&allowPublicKeyRetrieval=true" --rdbms:user admin --rdbms:password ***REMOVED*** --using cypher:fromSQL --unwind-batch-size 1000 --tx-batch-size 10000 --neo4j:url "bolt://192.168.2.4:7687" --neo4j:user neo4j --neo4j:password ***REMOVED*** --mapping-file /d/mysql_cy_db_mapping.json --debug