#!/usr/bin/env python3
import argparse
import os
import stat
import share
from pathlib import Path

if __name__ == '__main__':
    private_key = Path(__file__).parent.joinpath("___temp/private-key").as_posix()
    os.chmod(private_key, stat.S_IRUSR)
    ansible_hosts = Path(__file__).parent.joinpath("hosts").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True)
    parser.add_argument('-t', required=True)
    parser.add_argument('-p', action="store_true")
    args = parser.parse_args()
    ansible_file = Path(__file__).parent.joinpath(args.i + ".yml").as_posix()
    ansible_cmd = share.arr_param_to_str([
        "ansible-playbook",
        "--inventory", ansible_hosts, ansible_file,
        "--tags", args.t,
        "--ask-pass" if args.p else ["--private-key", private_key],
        "--flush-cache",
        "--step",
        "--verbose"
    ])
    print(ansible_cmd)
    share.execute_cmd(ansible_cmd)
