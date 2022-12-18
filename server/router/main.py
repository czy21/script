#!/usr/bin/env python3
import argparse
import pathlib

import share

from utility import (
    collection as collection_util
)


def uci_bak_config_section_cmd(config_name, kind: str, section: str, output_file: pathlib.Path):
    _uci_cmd = [
        "uci show {0}".format(config_name),
        "grep '{0}.{1}'".format(config_name, "@{0}".format(kind) if section is None else section)
    ]
    _sed_cmd = [
        "sed"
    ]
    if section is None:
        _sed_cmd.append("-e 's|\\[.*\\]|[-1]|g'")
        _sed_cmd.append("-e 's|^{0}.{1}|set \\0|g'".format(config_name, "@{0}".format(kind) if section is None else section))
        _sed_cmd.append("-e 's|.*={1}|add {0} {1}|g'".format(config_name, kind))
    else:
        _sed_cmd.append("-e 's|^{0}|set \\0|g'".format(config_name))
    _uci_cmd.append(collection_util.flat_to_str(_sed_cmd))
    return collection_util.flat_to_str(_uci_cmd, delimiter=" | ") + " >> {0}".format(output_file)


def get_cmds(role_title: str,
             role_name: str,
             role_path: pathlib.Path,
             role_output_path: pathlib.Path,
             role_env: dict,
             namespace: str,
             args: argparse.Namespace,
             **kwargs) -> list[str]:
    role_restore_script_uci = role_path.joinpath("___temp/restore").joinpath("{0}.uci".format(role_name))
    _cmds = []
    if args.command == "install":
        for c in role_env.get("param_config"):
            _kind: str = c.get("kind")
            _section: str = c.get("section")
            if _section is None:
                _cmds.append("while uci -q delete {0}.@{1}[0]; do :; done".format(role_name, _kind))
                _cmds.append("cat {0} | uci batch".format(role_restore_script_uci.as_posix()))
            else:
                _section_del_cmd = collection_util.flat_to_str([
                    "uci show {0}".format(role_name),
                    "grep '^{0}.{1}\\(.*\\)={2}'".format(role_name, "@{0}".format(_kind) if _section is None else _section, _kind),
                    collection_util.flat_to_str([
                        "sed",
                        "-e 's|={0}|\\1|g'".format(_kind),
                        "-e 's|^{0}|delete \\0|g'".format(role_name)
                    ]),
                ], delimiter=" | ")
                _cmds.append("({0};cat {1};echo;) | cat | uci batch".format(_section_del_cmd, role_restore_script_uci.as_posix()))
            _cmds.append("uci commit {0}".format(role_name))
    if args.command == "backup":
        role_bak_path = role_path.joinpath("___temp")
        role_bak_script_uci = role_bak_path.joinpath("{0}.uci.bak".format(role_name))
        _bak_cmds = [
            "mkdir -p {0}".format(role_bak_path.as_posix()),
            "cat /dev/null > {0}".format(role_bak_script_uci)
        ]
        for c in role_env.get("param_config"):
            _kind: str = c.get("kind")
            _section: str = c.get("section")
            _bak_cmds.append(uci_bak_config_section_cmd(role_name, _kind, _section, role_bak_script_uci))
        _cmds.append(share.echo_action(role_title, "backup"))
        _cmds.append(_bak_cmds)
    return _cmds


if __name__ == '__main__':
    installer = share.Installer(pathlib.Path(__file__).parent, get_cmds)
    installer.run()
