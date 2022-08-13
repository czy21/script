#!/usr/bin/env python3
import argparse
import logging
import pathlib

import share
import yaml

from utility import collection as collection_util, file as file_util, yaml as yaml_util, log as log_util

logger = logging.getLogger()

if __name__ == '__main__':
    log_util.init_logger()
    env_dict = yaml_util.load(file_util.read_text(pathlib.Path(__file__).parent.joinpath("env.yaml")))
    file_util.write_text(pathlib.Path(__file__).parent.joinpath("vars/env.yml"), yaml.dump(env_dict))

    private_key = pathlib.Path(__file__).parent.joinpath("___temp/private-key").as_posix()
    ansible_hosts = pathlib.Path(__file__).parent.joinpath("ansible-hosts").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--param', nargs="+", default=[])
    parser.add_argument('-i', required=True)
    parser.add_argument('-t', required=True)
    parser.add_argument('-k', action="store_true")
    parser.add_argument('-u', '--user', type=str, default=env_dict["param_user_ops"])
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    ansible_inventory_file = pathlib.Path(__file__).parent.joinpath(args.i + ".yml").as_posix()

    _cmds = ["chmod 600 {0}".format(private_key)]
    ansible_playbook_cmd = [
        "ANSIBLE_SUDO_PASS=0",
        "ANSIBLE_HOST_KEY_CHECKING=0",
        "ANSIBLE_FORCE_COLOR=1",
        "ansible-playbook",
        "--ssh-common-args \'-o StrictHostKeyChecking=no\'",
        "--ssh-extra-args \'-o StrictHostKeyChecking=no\'",
        "--scp-extra-args \'-o StrictHostKeyChecking=no\'",
        "--inventory", ansible_hosts, ansible_inventory_file,
        "--tags", args.t,
        "--ask-pass" if args.k else ["--private-key", private_key],
        "--flush-cache",
        "--step",
    ]
    if args.param:
        param_extra_iter = iter(args.param)
        ansible_playbook_cmd.append("-e \"{0}\"".format(" ".join(["{0}={1}".format(k, v) for k, v in dict(zip(param_extra_iter, param_extra_iter)).items()])))
    if args.user:
        ansible_playbook_cmd.append("--user {0}".format(args.user))
    if args.debug:
        ansible_playbook_cmd.append("--verbose")
    _cmds.append(collection_util.flat_to_str(ansible_playbook_cmd))
    share.run_cmd(collection_util.flat_to_str(_cmds, delimiter=" && "), is_log=False)
