#!/usr/bin/env python3

import argparse
import logging
import pathlib

from server import share

logger = logging.getLogger()


class SynoRole(share.AbstractRole):

    def __init__(self, context: share.RoleContext) -> None:
        super().__init__(context)
        self.role_conf_path = context.role_output_path.joinpath("conf")
        self.role_init_sh = context.role_output_path.joinpath("init.sh")

    def install(self) -> list[str]:
        return ["bash {}".format(self.role_init_sh.as_posix())]

    def build(self) -> list[str]:
        return []

    def delete(self) -> list[str]:
        return []

    def backup(self) -> list[str]:
        return []

    def restore(self) -> list[str]:
        return []

    def push(self) -> list[str]:
        return []


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, SynoRole, role_deep=1).run()
