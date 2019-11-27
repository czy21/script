#!/bin/bash
export JAVA_HOME=/usr/java/jdk-12.0.1
export JAVA=$JAVA_HOME/bin/java

erp_pid=`ps -ef | grep java | grep erp- | grep -v grep | awk '{print $2}'`
erp_version=`ps -ef | grep java | grep erp- | grep -v grep | awk '{print $10}'`
case "$1" in
	"-d")
	if [ -n "$erp_pid" ];
	then
	 kill -9 $erp_pid
	 rm -rf  $erp_version
	 echo "kill api success"
	fi;;
	"-u") 
	cur_erp=`find ./ -name "*.jar"`
	nohup $JAVA -jar $cur_erp --spring.profiles.active=prod > erp.log &
	echo "start api success";;
esac


