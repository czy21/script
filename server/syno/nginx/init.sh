#!/bin/bash

sudo cp -rv {{ param_role_output_path }}/conf/cert/* /usr/syno/etc/www/certificate/
sudo cp -rv {{ param_role_output_path }}/conf/conf.d/* /etc/nginx/conf.d/