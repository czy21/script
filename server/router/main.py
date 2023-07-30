#!/usr/bin/env python3
import argparse
import json
import pathlib
import re

import share
import yaml

from utility import (
    collection as collection_util,
    file as file_util
)


def format_config(config_type: str, config_section):
    return "@{0}".format(config_type) if config_section is None else config_section


def uci_bak_config_cmd(name, kind: str, section: str, output_file: pathlib.Path):
    _uci_cmd = [
        "uci show {0}".format(name),
        "grep -E '{0}.{1}'".format(name, format_config(kind, section))
    ]
    _sed_cmd = [
        "sed"
    ]
    if section is None:
        _sed_cmd.append("-e 's|\\[.*\\]|[-1]|g'")
        _sed_cmd.append("-e 's|^{0}.{1}|set \\0|g'".format(name, format_config(kind, section)))
        _sed_cmd.append("-e 's|.*={1}|add {0} {1}|g'".format(name, kind))
    else:
        _sed_cmd.append("-e 's|^{0}|set \\0|g'".format(name))
    _uci_cmd.append(collection_util.flat_to_str(_sed_cmd))
    _uci_cmd.append("while IFS='=' read -r k v;do "
                    "IFS=\" \"; vl=0;for e in $v;do let vl+=1;done;"
                    "if [ \"$vl\" -gt 1 ];then for e in $v;do echo $k=$e|sed 's|^set|add_list|g';done;elif [ -z $v ];then echo $k;else echo $k=$v;fi;"
                    "done")
    return collection_util.flat_to_str(_uci_cmd, delimiter=" | ") + " >> {0}".format(output_file)


def get_cmds(root_path: pathlib.Path,
             role_title: str,
             role_name: str,
             role_path: pathlib.Path,
             role_output_path: pathlib.Path,
             role_env: dict,
             namespace: str,
             args: argparse.Namespace,
             **kwargs) -> list[str]:
    role_script_uci = role_path.joinpath("___temp").joinpath("script.uci")
    role_script_uci_bak = role_path.joinpath("___temp").joinpath("script.uci.bak")
    if args.command == share.Command.restore.value:
        role_script_uci = role_script_uci_bak
    role_init_sh = role_output_path.joinpath("init.sh")
    param_uci_config = role_env.get("param_uci_config")
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
