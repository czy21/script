#!/bin/sh
exec spawn-fcgi -s /var/run/fcgiwrap.socket -u nginx -g nginx /usr/bin/fcgiwrap -f > /dev/stdout 2> /dev/stderr