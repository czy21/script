#!/usr/bin/env python3
import argparse
import os
import pathlib
import stat

import share
import yaml

from utility import collection as collection_util, file as file_util, yaml as yaml_util

if __name__ == '__main__':
    env_dict = yaml_util.load(file_util.read_text(pathlib.Path(__file__).parent.joinpath("env.yaml")))
    file_util.write_text(pathlib.Path(__file__).parent.joinpath("vars/env.yml"), yaml.dump(env_dict))

    with open(pathlib.Path(__file__).parent.joinpath("env.yaml").as_posix(), mode="r", encoding="utf-8") as ef:
        with open(pathlib.Path(__file__).parent.joinpath("vars/env.yml"), mode="w", encoding="utf-8") as vf:
            yaml.dump(yaml.full_load(ef), vf)

    private_key = pathlib.Path(__file__).parent.joinpath("___temp/private-key").as_posix()
    os.chmod(private_key, stat.S_IRUSR)
    ansible_hosts = pathlib.Path(__file__).parent.joinpath("ansible-hosts").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--param', nargs="+", default=[])
    parser.add_argument('-i', required=True)
    parser.add_argument('-t', required=True)
    parser.add_argument('-k', action="store_true")
    parser.add_argument('-u', '--user', type=str, default=env_dict["param_user_ops"])
    args = parser.parse_args()
    print(args)
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
    if args.param:
        param_extra_iter = iter(args.param)
        _param = " ".join(["{0}={1}".format(k, v) for k, v in dict(zip(param_extra_iter, param_extra_iter)).items()])
        ansible_cmd.append("-e \"{0}\"".format(_param))
    if args.user:
        ansible_cmd.append("--user {0}".format(args.user))
    share.run_cmd(collection_util.flat_to_str(ansible_cmd))
