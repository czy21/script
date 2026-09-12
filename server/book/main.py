#!/usr/bin/env python3
import argparse
import logging
import pathlib
import sys

import yaml

from server import share
from util import (
    collection as collection_util,
    file as file_util,
    log as log_util,
    yaml as yaml_util,
)

logger = logging.getLogger()

if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path)
    private_key = installer.tmp_path.joinpath("private-key")
    ansible_host_file = root_path.joinpath("ansible-host").as_posix()
    installer.arg_parser = argparse.ArgumentParser(formatter_class=share.ArgParseHelpFormatter, conflict_handler="resolve")
    installer.set_common_argument(installer.arg_parser)
    installer.arg_parser.add_argument('--ansible-host', required=False, type=str, help="ansible host file (default=ansible-host)")
    installer.arg_parser.add_argument('-f', '--file', required=True, type=str, help="inventory file")
    installer.arg_parser.add_argument('--list-tags', action="store_true", help="list all available tags")
    installer.arg_parser.add_argument('--list-tasks', action="store_true", help="list all available tasks")

    installer.arg_parser.add_argument('-t', '--tags', required=False, type=str, help="t1,t2")
    installer.arg_parser.add_argument('-k', '--ask-pass', action="store_true", help="ask for connection password")
    installer.arg_parser.add_argument('-u', '--user', required=False, type=str, help="connect as this user (default=[param_user])")
    installer.arg_parser.add_argument('--no-step', action="store_true", help="disable one-step-at-a-time")
    args = installer.arg_parser.parse_args()
    args.param = dict(args.param)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    if not private_key.exists():
        logger.error("ssh private-key not exists")
        sys.exit(0)
    private_key = private_key.as_posix()
    env_dict = installer.load_env_file(args.env_active, args.param)
    file_util.write_text(root_path.joinpath("vars/env.yml"), yaml_util.dump(env_dict))
    if not args.user:
        args.user = env_dict["param_user"]
    if args.ansible_host:
        ansible_host_file = root_path.joinpath(args.ansible_host).as_posix()
    ansible_inventory_file = pathlib.Path(args.file).as_posix() if pathlib.Path(args.file).is_absolute() else root_path.joinpath(args.file).as_posix()
    _cmds = ["chmod 600 {0}".format(private_key)]
    ansible_playbook_cmd = [
        "LC_ALL=C.UTF-8",
        "ANSIBLE_DEPRECATION_WARNINGS=0",
        "ANSIBLE_SUDO_PASS=0",
        "ANSIBLE_HOST_KEY_CHECKING=0",
        "ANSIBLE_FORCE_COLOR=1",
        "ANSIBLE_CALLBACK_RESULT_FORMAT=yaml",
        "ANSIBLE_CHECK_MODE_MARKERS=yes",
        f"ANSIBLE_LOG_PATH={root_path.joinpath("build.log").as_posix()}",
        "$HOME/.python3/bin/ansible-playbook",
        "--ssh-common-args \'-o StrictHostKeyChecking=no\'",
        "--ssh-extra-args \'-o StrictHostKeyChecking=no\'",
        "--scp-extra-args \'-o StrictHostKeyChecking=no\'",
        "--inventory", ansible_host_file, ansible_inventory_file,
        "--flush-cache",
        "--ask-pass" if args.ask_pass else ["--private-key", private_key]
    ]

    if args.list_tags:
        ansible_playbook_cmd.append("--list-tags")
    if args.list_tasks:
        ansible_playbook_cmd.append("--list-tasks")
    if args.tags:
        ansible_playbook_cmd.append(f"--tags {args.tags}")
    if args.user:
        ansible_playbook_cmd.append(f"--user {args.user}")
    if args.param:
        ansible_playbook_cmd.append(f"--extra-vars \"{args.param}\"")

    if not args.no_step:
        ansible_playbook_cmd.append("--step")
    ansible_playbook_cmd.append("-v")
    if args.dry_run:
        ansible_playbook_cmd.append("--check")
    _cmds.append(collection_util.flat_to_str(ansible_playbook_cmd))
    share.execute(collection_util.flat_to_str(_cmds, delimiter=" && "), is_return=False, dry_run=False)
