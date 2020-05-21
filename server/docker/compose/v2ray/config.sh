#!/usr/bin/env bash

set -e

sudo mkdir -p /data/volumes/v2ray/

sudo tee /data/volumes/v2ray/config.json <<-'EOF'
{
    "inbounds": [
        {
            "port": 9000,
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "id": "e85f98fb-83b4-4234-a51f-85df46403a8e",
                        "alterId": 4
                    }
                ],
                "detour": {
                    "to": "dynamicPort"
                }
            }
        },
        {
            "protocol": "vmess",
            "port": "10000-20000",
            "tag": "dynamicPort",
            "settings": {
                "default": {
                    "alterId": 64
                }
            },
            "allocate": {
                "strategy": "random",
                "concurrency": 2,
                "refresh": 3
            }
        }
    ],
    "outbounds": [
        {
            "protocol": "freedom",
            "settings": {}
        }
    ]
}
EOF