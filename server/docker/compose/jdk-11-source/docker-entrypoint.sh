#!/bin/bash
set -e

service ssh start

exec "$@"