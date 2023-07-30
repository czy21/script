#!/usr/bin/env python3
import argparse
import json
import pathlib

import share
from utility import (
    file as file_util
)


def get_cmds(root_path: pathlib.Path,
             role_title: str,
             role_name: str,
             role_path: pathlib.Path,
             role_output_path: pathlib.Path,
             role_env: dict,
             namespace: str,
             args: argparse.Namespace,
             **kwargs) -> list[str]:
    role_init_sh = role_output_path.joinpath("init.sh")
    _cmds = []
    if role_init_sh.exists():
        _cmds.append("bash {}".format(role_init_sh.as_posix()))
    role_env_output_json = role_output_path.joinpath("env.json")
    file_util.write_text(role_env_output_json, json.dumps(role_env))
    _cmds.append("lua {0} --command {1} --env-file {2}".format(root_path.joinpath("role.lua"), args.command, role_env_output_json.as_posix()))
    return _cmds


if __name__ == '__main__':
    installer = share.Installer(pathlib.Path(__file__).parent, get_cmds)
    installer.run()
