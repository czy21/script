#!/bin/bash
set -e

HOST_IPV4="{{ param_ansible_host_ipv4 }}"
LEAD_IPV4="{{ param_ansible_lead_ipv4 }}"

STATE="BACKUP"
INTERFACE="{{ param_ansible_host_iface }}"
ROUTER_ID=51
PRIORITY=50
AUTH_PASS=42
APISERVER_VIP={{ param_k8s_ha_api_server_vip }}
APISERVER_SRC_PORT=6443
APISERVER_DST_PORT={{ param_k8s_ha_api_server_dst_port }}

if [ "${LEAD_IPV4}" = "${HOST_IPV4}" ];then
  STATE="MASTER"
  PRIORITY=100
fi

sudo tee /etc/keepalived/keepalived.conf << EOF
! /etc/keepalived/keepalived.conf
! Configuration File for keepalived
global_defs {
    router_id LVS_DEVEL
}
vrrp_script check_apiserver {
  script \"/etc/keepalived/check_apiserver.sh\"
  interval 3
  weight -2
  fall 10
  rise 2
}

vrrp_instance VI_1 {
    state ${STATE}
    interface ${INTERFACE}
    virtual_router_id ${ROUTER_ID}
    priority ${PRIORITY}
    authentication {
        auth_type PASS
        auth_pass ${AUTH_PASS}
    }
    virtual_ipaddress {
        ${APISERVER_VIP}
    }
    track_script {
        check_apiserver
    }
}
EOF

sudo tee /etc/keepalived/check_apiserver.sh << EOF
#!/bin/sh

errorExit() {
    echo "*** $*" 1>&2
    exit 1
}

curl --silent --max-time 2 --insecure https://localhost:${APISERVER_DST_PORT}/ -o /dev/null || errorExit "Error GET https://localhost:${APISERVER_DST_PORT}/"
if ip addr | grep -q ${APISERVER_VIP}; then
    curl --silent --max-time 2 --insecure https://${APISERVER_VIP}:${APISERVER_DST_PORT}/ -o /dev/null || errorExit "Error GET https://${APISERVER_VIP}:${APISERVER_DST_PORT}/"
fi
EOF

sudo tee /etc/haproxy/conf.d/k8s.cfg << EOF
#---------------------------------------------------------------------
# apiserver frontend which proxys to the control plane nodes
#---------------------------------------------------------------------
frontend apiserver
    bind *:${APISERVER_DST_PORT}
    mode tcp
    option tcplog
    default_backend apiserver

#---------------------------------------------------------------------
# round robin balancing for apiserver
#---------------------------------------------------------------------
backend apiserver
    retries                 1
    timeout http-request    10s
    timeout queue           20s
    timeout connect         5s
    timeout client          20s
    timeout server          20s
    timeout http-keep-alive 10s
    timeout check           10s
    option httpchk GET /healthz
    http-check expect status 200
    mode tcp
    option ssl-hello-chk
    balance     roundrobin
{% for t in param_ansible_hosts %}
      server {{ t['name'] }} {{ t['ip'] }}:${APISERVER_SRC_PORT} check
{% endfor %}
EOF