#!/usr/bin/env python3
import argparse
import os
import pathlib
import stat

import share
import yaml

from utility import collection as collection_util

if __name__ == '__main__':
    yaml.add_constructor('!join', lambda loader, node: "".join(loader.construct_sequence(node, deep=True)))
    with open(pathlib.Path(__file__).parent.joinpath("env.yaml").as_posix(), mode="r", encoding="utf-8") as ef:
        with open(pathlib.Path(__file__).parent.joinpath("vars/env.yml"), mode="w", encoding="utf-8") as vf:
            yaml.dump(yaml.full_load(ef), vf)

    private_key = pathlib.Path(__file__).parent.joinpath("___temp/private-key").as_posix()
    os.chmod(private_key, stat.S_IRUSR)
    ansible_hosts = pathlib.Path(__file__).parent.joinpath("ansible-hosts").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True)
    parser.add_argument('-t', required=True)
    parser.add_argument('-k', action="store_true")
    parser.add_argument('-u', '--user', type=str, default="bruce")
    args = parser.parse_args()
    ansible_file = pathlib.Path(__file__).parent.joinpath(args.i + ".yml").as_posix()

    ansible_cmd = [
        "ANSIBLE_SUDO_PASS=0",
        "ANSIBLE_HOST_KEY_CHECKING=0",
        "ANSIBLE_FORCE_COLOR=1",
        "ansible-playbook",
        "--inventory", ansible_hosts, ansible_file,
        "--tags", args.t,
        "--ask-pass" if args.k else ["--private-key", private_key],
        "--flush-cache",
        "--step",
        # "--verbose"
    ]
    if args.user:
        ansible_cmd.append("--user {0}".format(args.user))
    share.run_cmd(collection_util.flat_to_str(ansible_cmd))
