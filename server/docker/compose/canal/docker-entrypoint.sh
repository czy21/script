#!/bin/bash
set -e

service ssh start

${CANAL_HOME}/bin/startup.sh
exec "$@"