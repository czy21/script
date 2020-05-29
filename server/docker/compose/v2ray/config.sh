#!/bin/bash

set -e

sudo mkdir -p /data/volumes/v2ray/

sudo tee /data/volumes/v2ray/config.json <<-'EOF'
{
    "inbounds": [
        {
            "port": 9000,
            "listen": "127.0.0.1",
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "id": "e85f98fb-83b4-4234-a51f-85df46403a8e",
                        "alterId": 4
                    }
                ]
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