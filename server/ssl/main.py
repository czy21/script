#!/usr/bin/env python3
import pathlib

import share

from utility import collection as collection_util


def invoke(role_title: str, role_path: pathlib.Path, **kwargs):
    args = kwargs["args"]
    root_path = kwargs["root_path"]
    role_name = role_path.name

    _cmds = []
    role_build_sh = role_path.joinpath("build.sh")
    if args.build == "build.sh":
        _cmds.append(share.echo_action(role_title, "build.sh"))
        if role_build_sh.exists():
            _cmds.append("sh {0}".format(role_build_sh.as_posix()))
            root_role_tmp_path = root_path.joinpath("___temp").joinpath(role_name)
            _cmds.append("mkdir -p {0}".format(root_role_tmp_path))
            _cmds.append("cp -r {0}/* {1}/".format(role_path.joinpath("___temp"), root_role_tmp_path))
    _cmd_str = collection_util.flat_to_str([_cmds, "echo \n"], delimiter=" && ")
    share.run_cmd(_cmd_str)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke)
    installer.run()
