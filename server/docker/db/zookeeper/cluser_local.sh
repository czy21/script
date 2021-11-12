#!/bin/bash

NL=$'\n'

cfg_template='
tickTime=2000
initLimit=10
syncLimit=5'

zk_count=1
servers=''
for i in `seq 1 $zk_count`; do
  servers=${servers}"server.${i}=127.0.0.1:218${i}:388${i}"${NL}
done

for i in `seq 1 $zk_count`; do
  zk_seq="/opt/zk/"$i
  mkdir -p ${zk_seq}
  cp -r $ZK_TMP/* ${zk_seq}
  cfg=${cfg_template}${NL}"dataDir="${zk_seq}"/data"${NL}"dataLogDir="${zk_seq}"/log"${NL}"clientPort=218${i}"${NL}${servers}
  cat > ${zk_seq}/conf/zoo.cfg <<EOF
  ${cfg}
EOF
  mkdir -p ${zk_seq}/data/
  cat > ${zk_seq}/data/myid <<EOF
${i}
EOF
done
rm -rf $ZK_TMP/
for i in `seq 1 $zk_count`; do
  zk_seq="/opt/zk/"$i
  ${zk_seq}/bin/zkServer.sh start
done