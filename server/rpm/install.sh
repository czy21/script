#!/bin/bash

# for machine version centos

# install to host machine
# bash install.sh --host user@host --install

# install to container
# bash install.sh --host user@host --install --container [container_name] --user [container_user]

root_dir="rpm"

dir=$(cd "$(dirname "$0")"; pwd)
dir=${dir}/___temp

mysql_version="8.0.21-1.el8"
mongo_version="rhel80-4.4.1"
neo4j_version="4.1.2-1"

while [[ $# -ge 1 ]];
do
	case $1 in
		--host)
			if [[ ! $2 ]] || [[ "$2" =~ ^"--".* ]]; then
			  echo -e "\033[31m$1 host is null \033[0m"
			  shift 1
        continue
      fi
      host=$2
      shift 2
      rm_sh='rm -rf $HOME/'"${root_dir}"'/'
      exec_sh='$HOME/'${root_dir}'/install.sh '$@''
      ssh ${host} "${rm_sh}" && scp -r ../${root_dir}/ ${host}:
      ssh ${host} "${exec_sh}"
      ssh ${host} "${rm_sh}"
      break
			;;
		--install)
		  if [[ ! $2 ]]; then

        # mysql
		    mysql_tmp=${dir}/mysql/ && mkdir -p ${mysql_tmp}

        wget -P ${mysql_tmp} https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-community-common-${mysql_version}.x86_64.rpm
        wget -P ${mysql_tmp} https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-community-libs-${mysql_version}.x86_64.rpm
        wget -P ${mysql_tmp} https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-community-client-${mysql_version}.x86_64.rpm

        rpm -ivh ${mysql_tmp}mysql-community-common-${mysql_version}.x86_64.rpm
        rpm -ivh ${mysql_tmp}mysql-community-libs-${mysql_version}.x86_64.rpm
        rpm -ivh ${mysql_tmp}mysql-community-client-${mysql_version}.x86_64.rpm

        # node
        node_version=v12.19.0

        mkdir -p /opt/nvm && git clone https://github.com/nvm-sh/nvm.git /opt/nvm

        source /opt/nvm/nvm.sh

        nvm install ${node_version}
        tee /etc/profile.d/nvm.sh <<-'EOF'
source /opt/nvm/nvm.sh
nvm use v12.19.0
EOF

        # yarn
        curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
        yum -y install yarn && yarn global add nrm

        # mssql
        # must use root login and exec
        curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/msprod.repo
        # need manual exec yum install
        yum remove mssql-tools unixODBC-utf16-devel
        # yum install mssql-tools unixODBC-devel
        # echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> /etc/bashrc && source /etc/bashrc

        # mongo
        mongo_tmp=${dir}/mongo/ && mkdir -p ${mongo_tmp}
        mongo_opt=/opt/mongo/

        # must use root login and exec
        wget -P ${mongo_tmp} https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-${mongo_version}.tgz
        mkdir -p ${mongo_opt} && sudo tar -zxvf ${mongo_tmp}mongodb-linux-x86_64-${mongo_version}.tgz --strip-components 1 -C ${mongo_opt}
        echo 'export PATH="$PATH:/opt/mongo/bin"' >> /etc/bashrc && source /etc/bashrc

        # cypher
#        rpm -ivh ${dir}/neo4j/cypher-shell-${neo4j_version}.noarch.rpm



        rm -rf ${HOME}/${root_dir}/
        shift 1
        continue
		  fi
      if [ $2 == "--container" ]; then
        container_name=$3
        shift 3
        user=""
        if [ $1 == "--user" ]; then
            user=$2
            shift 2
        fi
          sudo docker exec -i ${container_name} bash -c 'rm -rf $HOME/'"${root_dir}"'/'
          sudo docker cp $HOME/${root_dir}/ ${container_name}:${user}
          sudo docker exec -i ${container_name} bash -c 'bash $HOME/'"${root_dir}"'/install.sh --install'
      fi
			;;
		*)
		  echo -e "\033[31m$1 un_know input param \033[0m"
			break
			;;
	esac
done