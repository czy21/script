export HDFS_DATANODE_USER=root
export HDFS_NAMENODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export JAVA_HOME=/usr/local/openjdk-8
export HADOOP_OS_TYPE=${HADOOP_OS_TYPE:-$(uname -s)}
export HADOOP_OPTS="-Djava.library.path=${HADOOP_HOME}/lib/native"