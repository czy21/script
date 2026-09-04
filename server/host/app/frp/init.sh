#!/bin/bash

sudo mkdir -p /etc/frp/
sudo cp -rv {{ param_role_out_path }}/conf/* /etc/frp/

sudo cp -rv {{ param_role_out_path }}/frps.service /etc/systemd/system/frps.service

sudo systemctl enable frps --now
sudo systemctl restart frps