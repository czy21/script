#!/usr/bin/env python3
import pathlib

import share

from utility import collection as collection_util


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


def uci_del_config_section_cmd(config_name, kind: str, section: str):
    _uci_cmd = [
        "uci show {0}".format(config_name),
        "grep '^{0}.{1}\\(.*\\)={2}'".format(config_name, "@{0}".format(kind) if section is None else section, kind)
    ]
    _sed_cmd = [
        "sed",
        "-e 's|={0}|\\1|g'".format(kind),
        "-e 's|^{0}|delete \\0|g'".format(config_name)
    ]
    if section is None:
        _sed_cmd.append("-e '1!G;h;$!d'")
    _uci_cmd.append(collection_util.flat_to_str(_sed_cmd))
    return collection_util.flat_to_str(_uci_cmd, delimiter=" | ")


def invoke(role_title: str, role_path: pathlib.Path, role_env: dict, **kwargs):
    args = kwargs["args"]
    role_name = role_path.name
    role_script_uci = role_path.joinpath("script.uci")

    _cmds = []

    if args.install:
        for c in role_env.get("param_config"):
            _kind: str = c.get("kind")
            _section: str = c.get("section")
            _cmds.append("({0};{1};echo;) | cat | uci batch".format(uci_del_config_section_cmd(role_name, _kind, _section), "cat {0}".format(role_script_uci.as_posix())))
            _cmds.append("uci commit {0}".format(role_name))
    if args.action == "backup":
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
    share.run_cmd(collection_util.flat_to_str(_cmds, delimiter=" && "))


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke)
    installer.run()
