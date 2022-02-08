#!/bin/bash

# bash toolchain.sh -f backup -p [path] -d [dir name]
# bash toolchain.sh -f prune  -t [path] -m [file prefix] -n [month]

function backup() {
	local p_dir;
	local d_dir;
	while getopts "p:d:" opt;do
		case $opt in
			p) p_dir=$OPTARG;;
			d) d_dir=$OPTARG;;
		esac
	done;
	echo -e "${p_dir}/${d_dir}\033[32m backup started \033[0m"
	tar --use-compress-program=pigz -cpf ${p_dir}/backup/${d_dir}-$(date +%Y%m%d-%H%M).tar.gz -C ${p_dir} ${d_dir}
	echo -e "${p_dir}/${d_dir}\033[32m backup finished \033[0m"
}

function prune() {
	local target_path;
	local file_prefix;
	local minus_number;
	while getopts "t:m:n:" opt;do
		case $opt in
			t) target_path=$OPTARG;;
			m) file_prefix=$OPTARG;;
			n) minus_number=$OPTARG;;
			*) exit 1 ;;
		esac
	done;
	minus_month=$(date -d "-${minus_number} month" +%Y%m)
	if [ -z "${target_path}" ]; then
		echo "option requires an argument -- t";
		exit 1;
	fi
	if [ -z "${file_prefix}" ]; then
		echo "option requires an argument -- m";
		exit 1;
	fi
	echo -e "${p_dir}/${d_dir}\033[32m prune started \033[0m"
	find ${target_path} -name $file_prefix$minus_month -exec rm -rf{}\;
	echo -e "${p_dir}/${d_dir}\033[32m prune finished \033[0m"
}

while getopts "f:" opt;do
	case $opt in
		f)
		  func_name=$2;
		  ${func_name} $@;
		  break;
		;;
	esac
done