#!/bin/bash


sudo cp -rv {{ param_role_output_path }}/conf/* /etc/authelia/

sudo systemctl restart authelia