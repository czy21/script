#!/usr/bin/env python3
import argparse
import configparser
import io
import itertools
import pathlib

import share
import yaml


def get_section_keys(k, v): return v["section"] if v.get("section") else ['@' + k]


def echo_section(t, role_name, bak_conf):
    type_key: str = t[0]
    type_val: dict = t[1]
    section_keys = get_section_keys(type_key, type_val)
    return ["uci show {0} | grep -q '^{0}.{1}' && echo '[{1}]' >> {2} && uci show {0} | grep '^{0}.{1}' >> {2}".format(role_name, s, bak_conf.as_posix()) for s in section_keys]


def invoke(root_path: pathlib.Path, role_title: str, role_path: pathlib.Path, role_env_dict: dict, bak_path: pathlib.Path, **kwargs):
    args = kwargs["args"]
    role_name = role_path.name
    conf_file = role_path.joinpath("conf")
    meta_file = role_path.joinpath("meta.yml")
    if meta_file and meta_file.exists():
        with io.open(meta_file, "r", encoding="utf-8", newline="\n") as o_file:
            meta_dict = yaml.unsafe_load(o_file.read())

    _cmds = []
    if args.install:
        def prune_type(t):
            return ";".join([
                "type_total=$(uci show {0} | grep '^{0}\\(.*\\)={1}' | wc -l)",
                share.role_print("prune", "{0}.@{1}", "total:${{type_total}}"),
                "for i in $(seq ${{type_total}} -1 1);do uci del {0}.@{1}[$(($i-1))];done"
            ]).format(role_name, t)

        _cmds.append([
            share.role_print(role_title, "install"),
            [prune_type(t) for t in meta_dict.keys()],
            "uci -f {0} -m import {1}".format(conf_file.as_posix(), role_name),
            "uci commit {0}".format(role_name)
        ])
    if args.action == "backup":
        role_bak_path = role_path.joinpath("bak")
        role_bak_conf = role_bak_path.joinpath("conf")
        _bak_cmds = [
            "mkdir -p {0}".format(role_bak_path.as_posix()),
            [echo_section(t, role_name, role_bak_conf) for t in meta_dict.items()]
        ]
        share.run_cmd(share.flat_to_str(_bak_cmds, delimiter=" && "))

        type_parser = configparser.ConfigParser()
        type_parser.optionxform = str
        type_parser.read(role_bak_conf.as_posix())
        type_dict: dict = {i: {t[0]: t[1] for t in type_parser.items(i) if t[0].split(".").__len__() > 2} for i in type_parser.sections()}
        for m in meta_dict.items():
            m_type_key: str = m[0]
            m_type_val: dict = m[1]
            section_keys = get_section_keys(m_type_key, m_type_val)
            contents = []
            for sk in section_keys:
                if type_dict.get(sk):
                    for s in {k: {a[0].split(".")[2]: a[1] for a in l} for k, l in itertools.groupby(type_dict[sk].items(), key=lambda a: ".".join([a[0].split(".")[0], a[0].split(".")[1]])) if type_dict.get(sk)}.items():
                        section_key = s[0]
                        option_dict = s[1]
                        config_node = ["config", m_type_key]
                        if meta_dict.get(m_type_key).get("section"):
                            config_node.append("'{0}'".format(section_key.split(".")[1]))
                        option_text = "\n\t\t".join([" ".join(["option", o[0], o[1]]) for o in option_dict.items()])
                        contents.append(" ".join(config_node) + "\n\t\t" + option_text)
            with open(role_bak_conf, "w", encoding="utf-8") as t_file:
                t_file.write("\n".join(contents))
        _cmds.append(share.role_print(role_title, "backup")),
        _cmds.append("mkdir -p {0};cp -r {1}/* {0}/".format(bak_path.joinpath(role_name), role_bak_path))
    if args.action == "plugin":
        router_target_project_path = root_path.parent.joinpath(role_env_dict.get("param_router_project"))

        def get_plugin_checkout_cmd(source, target):
            return "svn checkout {0} {1}".format(source, target)

        for t in role_env_dict.get("param_router_plugin"):
            repo: str = t["repo"]
            apps: list = t["apps"]
            for a in apps:
                source_app_trunk = [repo.split(",")[0], "trunk"]
                if repo.split(",").__len__() == 2:
                    source_app_trunk.append(repo.split(",")[1])
                source_app_trunk.append(a)
                source_app_path = "/".join(source_app_trunk)
                target_app_path = router_target_project_path.joinpath(a)
                if not target_app_path.exists():
                    svn_checkout_cmd = " && ".join(["mkdir -p {0}".format(target_app_path.parent.parent), get_plugin_checkout_cmd(source_app_path, target_app_path)])
                    _cmds.append(svn_checkout_cmd)

    _cmd_str = share.flat_to_str(_cmds, delimiter=" && ")
    share.run_cmd(_cmd_str)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke)
    installer.run()
