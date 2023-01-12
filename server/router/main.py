#!/usr/bin/env python3
import argparse
import pathlib
import re

import share

from utility import (
    collection as collection_util
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


def get_cmds(role_title: str,
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
    if args.command in [share.Command.install.value, share.Command.restore.value]:
        if param_uci_config:
            for c in param_uci_config:
                _kind: str = c.get("type")
                _section: str = c.get("section")
                if _section is None:
                    _cmds.append("while uci -q delete {0}.@{1}[0]; do :; done".format(role_name, _kind))
                    _cmds.append("cat {0} | uci batch".format(role_script_uci.as_posix()))
                else:
                    _section_del_cmd = collection_util.flat_to_str([
                        "uci show {0}".format(role_name),
                        "grep -E '^{0}.{1}={2}'".format(role_name, format_config(_kind, _section), _kind),
                        collection_util.flat_to_str([
                            "sed",
                            "-e 's|={0}|\\1|g'".format(_kind),
                            "-e 's|^{0}|delete \\0|g'".format(role_name)
                        ]),
                    ], delimiter=" | ")
                    _cmds.append("({0};cat {1};echo;) | cat | uci batch".format(_section_del_cmd, role_script_uci.as_posix()))
                _cmds.append("uci commit {0}".format(role_name))
    if args.command == share.Command.backup.value:
        if param_uci_config:
            _bak_cmds = [
                "cat /dev/null > {0}".format(role_script_uci_bak)
            ]
            for c in param_uci_config:
                _kind: str = c.get("type")
                _section: str = c.get("section")
                _cmds.append(uci_bak_config_cmd(role_name, _kind, _section, role_script_uci_bak))

    return _cmds


if __name__ == '__main__':
    installer = share.Installer(pathlib.Path(__file__).parent, get_cmds)
    installer.run()
