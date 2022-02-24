#!/bin/bash

# bash toolchain.sh -f backup -p [path] -d [dir name]
# bash toolchain.sh -f prune  -t [path] -n [day]

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
	local target_regex;
	local minus_number;
	while getopts "t:n:" opt;do
		case $opt in
			t) target_regex=$OPTARG;;
			n) minus_number=$OPTARG;;
			*) exit 1 ;;
		esac
	done;
	minus_date=$(date -d "-${minus_number} day" +%Y%m%d)
	if [ -z "${target_regex}" ]; then
		echo "option requires an argument -- t";
		exit 1;
	fi
	local recent_date=$(find ${target_regex}-* -exec sh -c 'f={};file_date=$(basename ${f} | cut -d"-" -f3);echo ${file_date}' \; | xargs | perl -lane '$m<$_ and $m=$_ for @F; print $m')
	find ${target_regex}-* -exec sh -c 'f={};file_date=$(basename ${f} | cut -d"-" -f3);if [ ${file_date} -ne '${recent_date}' ] && [ $(date +%s -d ${file_date}) -ge '$(date +%s -d ${minus_date})' ]; then rm -fv $f;fi;' \;
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