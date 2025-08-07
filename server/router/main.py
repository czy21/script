#!/usr/bin/env python3
import json
import pathlib

from server import share
from utility import (
    file as file_util
)


class RouterRole(share.AbstractRole):

    def __init__(self, context: share.RoleContext) -> None:
        super().__init__(context)
        self.role_init_sh = context.role_output_path.joinpath("init.sh")
        self.role_env_output_json = context.role_output_path.joinpath("env.json")

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


def get_cmds(role: RouterRole) -> list[str]:
    _cmds = []
    if role.role_init_sh.exists():
        _cmds.append("bash {}".format(role.role_init_sh.as_posix()))
    file_util.write_text(role.role_env_output_json, json.dumps(role.context.role_env))
    _cmds.append("lua {0} --command {1} --env-file {2}".format(role.context.root_path.joinpath("role.lua"), role.context.args.command, role.role_env_output_json.as_posix()))
    return _cmds


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, RouterRole).run()
