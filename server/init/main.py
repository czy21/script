#!/usr/bin/env python3
import argparse
import logging
import pathlib
import sys

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
    pwd = pathlib.Path(__file__).parent
    build_path = pwd.joinpath("build")
    build_path.mkdir(exist_ok=True)
    tmp_path = pwd.joinpath("___temp")
    tmp_path.mkdir(exist_ok=True)
    log_util.init_logger()
    private_key = tmp_path.joinpath("private-key")
    if not private_key.exists():
        logger.error("ssh private-key not exists")
        sys.exit(0)
    private_key = private_key.as_posix()
    ansible_hosts = pwd.joinpath("ansible-hosts").as_posix()
    parser = argparse.ArgumentParser(formatter_class=share.CustomHelpFormatter, conflict_handler="resolve")
    share.Installer.set_common_argument(parser)
    parser.add_argument('--env-file', nargs="+", default=[], help="file1.yaml file2.yaml")
    parser.add_argument('-f', '--file', required=True, type=str, help="inventory file")
    parser.add_argument('-t', '--tag', required=True, type=str, help="t1,t2")
    parser.add_argument('-k', '--ask-pass', action="store_true", help="ask for connection password")
    parser.add_argument('-u', '--user', required=False, type=str, help="connect as this user (default=[param_user_ops])")
    parser.add_argument('--dry-run', action="store_true", help="don't make any changes")
    parser.add_argument('--no-step', action="store_true", help="disable one-step-at-a-time")
    args = parser.parse_args()
    env_file: pathlib.Path = pwd.joinpath("env.yaml")
    if not env_file.exists():
        logger.error("env file not exists")
        sys.exit(0)
    env_dict = share.load_env_file(env_file, args.env_file)
    file_util.write_text(pwd.joinpath("vars/env.yml"), yaml.dump(env_dict))
    if not args.user:
        args.user = env_dict["param_user_ops"]
    if args.debug:
        logger.setLevel(logging.DEBUG)

    ansible_inventory_file = pwd.joinpath("{0}.yml".format(args.file)).as_posix()
    ansible_log_file = pwd.joinpath("build/ansible.log").as_posix()
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
        ansible_playbook_cmd.append("-vv")
    if args.dry_run:
        ansible_playbook_cmd.append("--check")
    _cmds.append(collection_util.flat_to_str(ansible_playbook_cmd))
    share.execute(collection_util.flat_to_str(_cmds, delimiter=" && "), is_return=False, dry_run=args.dry_run)
