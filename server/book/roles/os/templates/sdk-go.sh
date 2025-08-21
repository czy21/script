#!/bin/bash
set -e

wget -O - https://go.dev/dl/go1.25.0.linux-amd64.tar.gz | sudo tar -zxf - -C /usr/local/