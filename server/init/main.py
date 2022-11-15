#!/usr/bin/env python3
import argparse
import logging
import pathlib

import share
import yaml

from utility import (
    collection as collection_util,
    file as file_util,
    yaml as yaml_util,
    log as log_util
)

logger = logging.getLogger()

if __name__ == '__main__':
    log_util.init_logger()
    env_dict = yaml_util.load(file_util.read_text(pathlib.Path(__file__).parent.joinpath("env.yaml")))
    file_util.write_text(pathlib.Path(__file__).parent.joinpath("vars/env.yml"), yaml.dump(env_dict))

    private_key = pathlib.Path(__file__).parent.joinpath("___temp/private-key").as_posix()
    ansible_hosts = pathlib.Path(__file__).parent.joinpath("ansible-hosts").as_posix()
    parser = argparse.ArgumentParser(formatter_class=share.CustomHelpFormatter, conflict_handler="resolve")
    share.Installer.set_common_argument(parser)
    parser.add_argument('-f', '--file', required=True, type=str, help="inventory file")
    parser.add_argument('-t', '--tag', required=True, type=str, help="t1,t2")
    parser.add_argument('-k', '--ask-pass', action="store_true", help="ask for connection password")
    parser.add_argument('-u', '--user', default=env_dict["param_user_ops"], type=str, help="connect as this user (default=[param_user_ops])")
    parser.add_argument('--check', action="store_true", help="don't make any changes")
    parser.add_argument('--no-step', action="store_true", help="disable one-step-at-a-time")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    ansible_inventory_file = pathlib.Path(__file__).parent.joinpath(args.file).as_posix()
    ansible_log_file = pathlib.Path(__file__).parent.joinpath("___temp/ansible.log").as_posix()
    _cmds = ["chmod 600 {0}".format(private_key)]
    ansible_playbook_cmd = [
        "ANSIBLE_SUDO_PASS=0",
        "ANSIBLE_HOST_KEY_CHECKING=0",
        "ANSIBLE_FORCE_COLOR=1",
        "ANSIBLE_STDOUT_CALLBACK=yaml",
        "ANSIBLE_CHECK_MODE_MARKERS=yes",
        "ANSIBLE_LOG_PATH={0}".format(ansible_log_file),
        "ansible-playbook",
        "--ssh-common-args \'-o StrictHostKeyChecking=no\'",
        "--ssh-extra-args \'-o StrictHostKeyChecking=no\'",
        "--scp-extra-args \'-o StrictHostKeyChecking=no\'",
        "--inventory", ansible_hosts, ansible_inventory_file,
        "--tags", args.tag,
        "--ask-pass" if args.ask_pass else ["--private-key", private_key],
        "--flush-cache"
    ]
    if args.param:
        ansible_playbook_cmd.append("-e \"{0}\"".format(args.param))
    if args.user:
        ansible_playbook_cmd.append("--user {0}".format(args.user))
    if not args.no_step:
        ansible_playbook_cmd.append("--step")
    if args.debug:
        ansible_playbook_cmd.append("--verbose")
    if args.check:
        ansible_playbook_cmd.append("--check")
    _cmds.append("echo -n '' > {0}".format(ansible_log_file))
    _cmds.append(collection_util.flat_to_str(ansible_playbook_cmd))
    share.execute(collection_util.flat_to_str(_cmds, delimiter=" && "), is_return=False, dry_run=args.dry_run)
