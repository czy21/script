#!/bin/bash

# bash toolchain.sh -f backup -p [path] -m [module]
# bash toolchain.sh -f prune  -t [path] -n [day]

function backup() {
	local p_dir;
	local modules;
	while getopts "p:m:" opt;do
		case $opt in
			p) p_dir=$OPTARG;;
			m) modules+=($OPTARG);;
		esac
	done;
	local now_time=$(date +%Y%m%d-%H%M)
	for m in ${modules[@]}; do
	  if [ -d "${p_dir}/${m}" ]; then
      tar --use-compress-program=pigz -cpf ${p_dir}/backup/${m}-${now_time}.tar.gz -C ${p_dir} ${m}
	  else
	    echo -e "${p_dir} not found ${m}"
	  fi
	done
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
	local recent_date=$(find ${target_regex}-* -exec sh -c 'f={};file_date=$(basename ${f} | cut -d"-" -f3);echo ${file_date}' \; | sort -rg | head -1)
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