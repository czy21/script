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
    root_path = kwargs["root_path"]
    role_name = role_path.name

    _cmds = []
    role_build_sh = role_path.joinpath("build.sh")
    if role_build_sh.exists():
        _cmds.append("sh {0}".format(role_build_sh.as_posix()))
        root_role_tmp_path = pathlib.Path(root_path).joinpath("___temp").joinpath(role_name)
        _cmds.append("mkdir -p {0}".format(root_role_tmp_path))
        _cmds.append("cp -r {0}/* {1}/".format(role_path.joinpath("___temp"), root_role_tmp_path))
    _cmd_str = share.flat_to_str([_cmds, "echo \n"], delimiter=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke, role_deep=1)
    installer.run()
