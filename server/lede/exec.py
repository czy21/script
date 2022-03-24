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


def invoke(role_title: str, role_path: pathlib.Path, **kwargs):
    args = kwargs["args"]
    bak_path: pathlib.Path = kwargs["bak_path"]
    role_name = role_path.name
    conf_file = role_path.joinpath("conf")
    meta_file = role_path.joinpath("meta.yml")
    with io.open(meta_file, "r", encoding="utf-8", newline="\n") as o_file:
        meta_dict = yaml.unsafe_load(o_file.read())

    _cmds = [
        share.role_print(role_title, args.a)
    ]
    if args.a == "install":
        def prune_type(t):
            return ";".join([
                "type_total=$(uci show {0} | grep '^{0}\\(.*\\)={1}' | wc -l)",
                share.role_print("prune", "{0}.@{1}", "total:${{type_total}}"),
                "for i in $(seq ${{type_total}} -1 1);do uci del {0}.@{1}[$(($i-1))];done"
            ]).format(role_name, t)

        _cmds.append([
            [prune_type(t) for t in meta_dict.keys()],
            "uci -f {0} -m import {1}".format(conf_file.as_posix(), role_name),
            "uci commit {0}".format(role_name)
        ])
    if args.a == "backup":
        role_bak_path = role_path.joinpath("bak")
        role_bak_conf = role_bak_path.joinpath("conf")
        _bak_cmds = [
            "mkdir -p {0}".format(role_bak_path.as_posix()),
            [echo_section(t, role_name, role_bak_conf) for t in meta_dict.items()]
        ]
        share.execute_cmd(share.flat_to_str(_bak_cmds, delimiter=" && "))

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
        _cmds.append("mkdir -p {0};cp -r {1}/* {0}/".format(bak_path.joinpath(role_name), role_bak_path))

    _cmd_str = share.flat_to_str(_cmds, delimiter=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    bak_path = pathlib.Path(__file__).parent.joinpath("___temp/bak")
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", default=[])
    parser.add_argument('-a', type=str, required=True)

    args = parser.parse_args()
    selected_option = share.select_option()
    share.execute(selected_option["role_dict"], invoke, bak_path=bak_path, args=args)