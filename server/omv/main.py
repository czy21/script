#!/usr/bin/env python3
import pathlib

from server import share


class OpenMediaValueRole(share.AbstractRole):

    def __init__(self, context: share.RoleContext) -> None:
        super().__init__(context)
        self.role_init_sh = context.role_output_path.joinpath("init.sh")

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


def get_cmds(role: OpenMediaValueRole) -> list[str]:
    _cmds = []
    if role.role_init_sh.exists():
        _cmds.append("bash {}".format(role.role_init_sh.as_posix()))
    return _cmds


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, OpenMediaValueRole).run()
