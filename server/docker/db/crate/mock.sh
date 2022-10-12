#!/bin/bash

values=()
for ((i=1;i<=1000;i++));do
  values=("${values[@]}" "('${i}')")
done
values=`echo ${values[@]} | sed 's| |,|g'`
for ((i=1;i<=$1;i++));do
   .python3/bin/crash --hosts 192.168.2.18:4201 --command "INSERT INTO user_mock (name) VALUES ${values}"
done