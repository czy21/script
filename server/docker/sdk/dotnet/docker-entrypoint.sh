#!/bin/bash

chmod +x ${API_FILE}
echo "${DOTNET_OPTS}" | xargs ${API_FILE}