#!/usr/bin/env python3
import json
import pathlib

from server import share
from utility import (
    file as file_util
)


class RouterRole(share.AbstractRole):

    def __init__(self,
                 home_path: pathlib.Path = None,
                 root_path: pathlib.Path = None,
                 namespace: str = None,
                 role_title: str = None,
                 role_name: str = None,
                 role_path: pathlib.Path = None,
                 role_output_path: pathlib.Path = None,
                 role_env: dict = None,
                 role_env_output_file: pathlib.Path = None,
                 args=None) -> None:
        super().__init__(home_path, root_path, namespace, role_title, role_name, role_path, role_output_path, role_env, role_env_output_file, args)
        self.role_init_sh = role_output_path.joinpath("init.sh")
        self.role_env_output_json = role_output_path.joinpath("env.json")

    def install(self) -> list[str]:
        return get_cmds(self)

    def build(self) -> list[str]:
        return get_cmds(self)

    def delete(self) -> list[str]:
        return get_cmds(self)

    def backup(self) -> list[str]:
        return get_cmds(self)

    def restore(self) -> list[str]:
        return get_cmds(self)

    def push(self) -> list[str]:
        return get_cmds(self)


def get_cmds(router_role: RouterRole) -> list[str]:
    _cmds = []
    if router_role.role_init_sh.exists():
        _cmds.append("bash {}".format(router_role.role_init_sh.as_posix()))
    file_util.write_text(router_role.role_env_output_json, json.dumps(router_role.role_env))
    _cmds.append("lua {0} --command {1} --env-file {2}".format(router_role.root_path.joinpath("role.lua"), router_role.args.command, router_role.role_env_output_json.as_posix()))
    return _cmds


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, RouterRole).run()
