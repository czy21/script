#!/usr/bin/env python3

import argparse
import logging
import pathlib

import urllib3.util

from server import share
from utility import (
    collection as collection_util,
    path as path_util,
    file as file_util,
    regex as regex_util,
    template as template_util
)

logger = logging.getLogger()


class SynoRole(share.AbstractRole):

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
                 args: argparse.Namespace = None) -> None:
        super().__init__(home_path, root_path, namespace, role_title, role_name, role_path, role_output_path, role_env, role_env_output_file, args)
        self.role_conf_path = role_output_path.joinpath("conf")
        self.role_init_sh = role_output_path.joinpath("init.sh")

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
