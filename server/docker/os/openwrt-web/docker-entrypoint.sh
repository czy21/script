#!/bin/sh

spawn-fcgi -s /var/run/fcgiwrap.socket -u nginx -g nginx /usr/bin/fcgiwrap

chmod 766 /var/run/fcgiwrap.socket

exec nginx -g "daemon off;"