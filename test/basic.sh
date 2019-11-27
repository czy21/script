#!/bin/bash

# $0: 脚本本身文件名称
# $1: 命令行第一个参数，$2为第二个，以此类推
# $*: 所有参数列表
# $@: 所有参数列表
# $#: 参数个数
# $$: 脚本运行时的PID
# $?: 脚本退出码
#python ./mongo.py
dir=$(cd "$(dirname "$0")";pwd)

#切换至当前目录
echo $dir
# 获取所有参数
echo "$@"

python db_source.py
#脚本暂停
read -n 1