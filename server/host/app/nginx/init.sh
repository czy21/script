#!/bin/bash

sudo cp -rv {{ param_role_out_path }}/conf/* /etc/nginx/ || true
sudo cp -rv {{ param_role_out_path }}/static/* /usr/share/nginx/ || true