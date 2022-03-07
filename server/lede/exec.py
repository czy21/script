#!/usr/bin/env python3
import argparse
import jinja2
import share

from pathlib import Path


def invoke(role_title: str, role_path: Path, **kwargs):
    args = kwargs["args"]

    conf_file = role_path.joinpath("conf")
    exec_file = role_path.joinpath("exec.sh")
    role_name = role_path.name
    _cmds = [
        share.role_print(role_title, args.a)
    ]
    if args.a == "install":
        _cmds.append("source {0}; prune".format(exec_file.as_posix()))
        _cmds.append("uci -f {0} -m import {1}".format(conf_file.as_posix(), role_name))
    _cmds.append("uci commit {0}".format(role_name))
    _cmd_str = share.arr_param_to_str(_cmds, separator=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
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
