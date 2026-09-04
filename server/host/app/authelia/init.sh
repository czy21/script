#!/bin/bash


sudo cp -rv {{ param_role_out_path }}/conf/* /etc/authelia/

sudo systemctl restart authelia