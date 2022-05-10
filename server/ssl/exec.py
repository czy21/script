#!/usr/bin/env python3
import argparse
import configparser
import io
import itertools
import pathlib

import jinja2
import share
import yaml


def invoke(role_title: str, role_path: pathlib.Path, **kwargs):
    args = kwargs["args"]

    env_dict: dict = kwargs["env_dict"]
    role_name = role_path.name

    for t in filter(lambda f: f.is_file() and share.exclude_match("({0})".format("|".join(args.excludes)), f.as_posix()), role_path.rglob("*")):
        with open(t, "r", encoding="utf-8", newline="\n") as sf:
            content = jinja2.Template(sf.read()).render(**env_dict)
            with open(t, "w", encoding="utf-8") as tf:
                tf.write(content)

    _cmds = []
    role_build_sh = role_path.joinpath("build.sh")
    if role_build_sh.exists():
        _cmds.append("bash {0}".format(role_build_sh.as_posix()))
        root_role_tmp_path = root_tmp_path.joinpath(role_name)
        _cmds.append("mkdir -p {0}".format(root_role_tmp_path))
        _cmds.append("cp -r {0}/* {1}/".format(role_path.joinpath("___temp"), root_role_tmp_path))
    _cmd_str = share.flat_to_str([_cmds, "echo \n"], delimiter=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    root_tmp_path = pathlib.Path(__file__).parent.joinpath("___temp")
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", default=[])

    args = parser.parse_args()
    selected_option = share.select_option()
    share.execute(selected_option, invoke, root_tmp_path=root_tmp_path, args=args)
