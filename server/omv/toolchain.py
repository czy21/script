#!/usr/bin/env python3
import argparse
import subprocess

nodes = [
    {
        "user": "bruce",
        "host": "192.168.2.21"
    },
    {
        "user": "bruce",
        "host": "192.168.2.22"
    },
    {
        "user": "bruce",
        "host": "192.168.2.25"
    },
    {
        "user": "bruce",
        "host": "192.168.2.26"
    },
]


def run_cmd(cmd):
    subprocess.Popen(cmd, shell=True).wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prune', nargs="+", default=[])
    args = parser.parse_args()
    for t in args.prune:
        if t == 'docker':
            docker_prune_cmd = " && ".join(["sudo docker container prune --force", "sudo docker image prune --all --force"])
            for i in nodes:
                _prune_cmd = "ssh -o StrictHostKeyChecking=no -i /root/.ssh/czy-rsa {0}@{1} '{2}'".format(
                    i["user"],
                    i["host"],
                    docker_prune_cmd
                )
                run_cmd(_prune_cmd)
            run_cmd(docker_prune_cmd)
