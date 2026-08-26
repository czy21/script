#!/usr/bin/env python3

import argparse
import requests,re

common_parser = argparse.ArgumentParser(add_help=False)
common_parser.add_argument('--endpoint')


def cmd_host_show(args):
    res = requests.get(f"{args.endpoint}/api/http/routers")
    for t in res.json():
        rule = t.get('rule')
        for d in args.domain:
            for h in re.findall(rf"Host\(`([^`]*{re.escape(d)})`\)", rule):
                print(f'{args.ip} {h}')


def cmd_host_push(args):
    consul_server = args.consul_server
    consul_token = args.consul_token
    consul_headers = {
        "X-Consul-Token": consul_token
    }

    traefik_endpoint = args.endpoint
    traefik_proxy_name = f'traefik-{args.proxy_name}'
    traefik_proxy_pass = args.proxy_pass
    requests.put(f"{consul_server}/v1/kv/traefik/http/services/{traefik_proxy_name}/loadbalancer/servers/0/url", headers=consul_headers, data=traefik_proxy_pass)

    res = requests.get(f"{traefik_endpoint}/api/http/routers")
    routers = res.json() if res.status_code == 200 else []
    routers = {
        f"traefik/http/routers/{t.get('name', '').replace('@file', f'@{traefik_proxy_name}')}": rule
        for t in routers
        if (rule := t.get('rule')) and 'Host' in rule
    }
    for k, v in routers.items():
        requests.put(f"{consul_server}/v1/kv/{k}/rule", headers=consul_headers, data=v)
        requests.put(f"{consul_server}/v1/kv/{k}/service", headers=consul_headers, data=f'{traefik_proxy_name}@consul')
    res = requests.get(f"{consul_server}/v1/kv/traefik/http/routers/?keys=true&separator=/", headers=consul_headers)
    routers_exists = res.json() if res.status_code == 200 else []
    routers_delete = [t for t in routers_exists if t.rstrip('/') not in routers] if routers else []
    for t in routers_delete:
        requests.delete(f"{consul_server}/v1/kv/{t}?recurse=true", headers=consul_headers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_host = subparsers.add_parser("host", help="")
    host_subparsers = p_host.add_subparsers(dest="host_cmd")
    host_subparsers.required = True

    p_host_show = host_subparsers.add_parser("show", parents=[common_parser])
    p_host_show.add_argument('--ip', required=True)
    p_host_show.add_argument('--domain', required=True, nargs="+", default=[])
    p_host_show.set_defaults(func=cmd_host_show)

    p_host_push = host_subparsers.add_parser("push", parents=[common_parser])
    p_host_push.add_argument('--consul-server')
    p_host_push.add_argument('--consul-token')
    p_host_push.add_argument('--proxy-name')
    p_host_push.add_argument('--proxy-pass')
    p_host_push.set_defaults(func=cmd_host_push)

    args = parser.parse_args()
    args.func(args)
