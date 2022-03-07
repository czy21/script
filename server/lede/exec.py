#!/usr/bin/env python3
import argparse
import jinja2
import share

from pathlib import Path


def invoke(role_title: str, role_path: Path, **kwargs):
    args = kwargs["args"]
    env_dict: dict = kwargs["env_dict"]
    common_sh: Path = kwargs["common_sh"]
    env_dict["param_common_sh"] = common_sh

    conf_file = role_path.joinpath("conf")
    exec_file = role_path.joinpath("exec.sh")
    role_name = role_path.name

    for t in filter(lambda f: f.is_file(), role_path.rglob("*")):
        with open(t, "r", encoding="utf-8", newline="\n") as r_file:
            content = jinja2.Template(r_file.read()).render(**env_dict)
            with open(t, "w", encoding="utf-8") as t_file:
                t_file.write(content)
    _cmds = [
        share.role_print(role_title, args.a)
    ]
    if args.a == "install":
        _cmds.append("source {0}".format(exec_file.as_posix()))
        _cmds.append("uci -f {0} -m import {1}".format(conf_file.as_posix(), role_name))
    _cmds.append("uci commit {0}".format(role_name))
    _cmd_str = share.arr_param_to_str(_cmds, separator=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    common_sh = Path(__file__).parent.joinpath("common.sh").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", default=[])
    parser.add_argument('-a', type=str, required=True)
    parser.add_argument("-t", default=2)
    parser.add_argument('-n')

    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    share.execute(selected_option["list"], invoke, common_sh=common_sh, args=args)
