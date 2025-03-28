#!/bin/bash

target_name=
target_code=
target_args=
target_dir=

while getopts "n:c:d:p::" opt;do
    case $opt in
        n) target_name=$OPTARG;;
        c) target_code=$OPTARG;;
        p) target_args=$OPTARG;;
        d) target_dir=$OPTARG;;
    esac
done;

echo ${target_args[@]}

if [ "$target_code" == "dotnet" ];then
    sudo tee /etc/systemd/system/${target_name}.service << EOF
[Unit]
Description=.NET Application
After=network.target

[Service]
WorkingDirectory=${target_dir}
ExecStart=${target_dir}/api $target_args
Restart=always
User=opsor

[Install]
WantedBy=multi-user.target

EOF
fi

sudo systemctl daemon-reload
sudo systemctl restart ${target_name}
sudo systemctl enable ${target_name}