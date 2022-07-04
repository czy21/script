#!/bin/bash
echo $@
function backup() {
  echo "backup"
}

function install() {
	echo "install"
}

while getopts $@ opt;do
	case $opt in
		f)
		  func_name=$2;
		  ${func_name} $@;
		  break;
		;;
	esac
done