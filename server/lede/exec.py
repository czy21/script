#!/usr/bin/env python3
import argparse
import io

import yaml
import jinja2
import share

from pathlib import Path


def invoke(role_title: str, role_path: Path, **kwargs):
    args = kwargs["args"]
    env_dict: dict = kwargs["env_dict"]
    role_name = role_path.name
    conf_file = role_path.joinpath("conf")
    meta_file = role_path.joinpath("meta.yml")
    with io.open(meta_file, "r", encoding="utf-8", newline="\n") as o_file:
        meta_dict: dict[str, object] = yaml.unsafe_load(o_file.read())
    role_types = meta_dict.keys()

    # for t in filter(lambda f: f.is_file(), role_path.rglob("*")):
    #     with open(t, "r", encoding="utf-8", newline="\n") as r_file:
    #         content = jinja2.Template(r_file.read()).render(**env_dict)
    #         with open(t, "w", encoding="utf-8") as t_file:
    #             t_file.write(content)
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

        _cmds.append([prune_type(t) for t in role_types])
        _cmds.append("uci -f {0} -m import {1}".format(conf_file.as_posix(), role_name))
        _cmds.append("uci commit {0}".format(role_name))
    if args.a == "backup":
        def backup():
            pass
    _cmd_str = share.arr_param_to_str(_cmds, separator=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    yaml.add_representer(str, lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, '|' if '\n' in data else ''))
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", default=[])
    parser.add_argument('-a', type=str, required=True)
    parser.add_argument("-t", default=2)
    parser.add_argument('-n')

    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    share.execute(selected_option["list"], invoke, args=args)
