#!/usr/bin/env python3
import argparse
import os
import pathlib
import stat

import share

if __name__ == '__main__':
    private_key = pathlib.Path(__file__).parent.joinpath("___temp/private-key").as_posix()
    os.chmod(private_key, stat.S_IRUSR)
    ansible_hosts = pathlib.Path(__file__).parent.joinpath("ansible-hosts").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True)
    parser.add_argument('-t', required=True)
    parser.add_argument('-k', action="store_true")
    args = parser.parse_args()
    ansible_file = pathlib.Path(__file__).parent.joinpath(args.i + ".yml").as_posix()
    ansible_cmd = share.flat_to_str([
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
    ])
    print(ansible_cmd)
    share.execute_cmd(ansible_cmd)
