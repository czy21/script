#!/bin/bash

# bash install.sh -p [path] -d [dir name]
# -p path
# -d dir name

while getopts "p:d:" opt;do
	case $opt in
		p) p_dir=$OPTARG;;
        d) d_dir=$OPTARG;;
	esac
done

echo -e "${p_dir}/${d_dir}\033[32m backup started \033[0m"
tar --use-compress-program=pigz -cpf ${p_dir}/backup/${d_dir}-$(date +%Y%m%d-%H%M).tar.gz -C ${p_dir} ${d_dir}
echo -e "${p_dir}/${d_dir}\033[32m backup finished \033[0m"