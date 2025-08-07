#!/usr/bin/env python3
import logging
import os
import pathlib
import re

from utility import (
    regex as regex_util,
    file as file_util
)

logger = logging.getLogger()


def dfs_dir(t_path: str, pattern: re = None) -> list:
    ret = []
    sort_target = os.listdir(t_path)
    sort_target.sort(key=lambda x: re.compile("^\\d+").match(x).group() if re.compile("^\\d+").match(x) else x)
    for sub_p in sort_target:
        tmp_path = join_path(t_path, sub_p)
        if os.path.isfile(tmp_path):
            if pattern:
                match = pattern.match(tmp_path)
                if match:
                    ret.append(match.group())
            else:
                ret.append(tmp_path)
        elif os.path.isdir(tmp_path):
            ret += dfs_dir(tmp_path, pattern=pattern)
    return ret


def join_path(*paths) -> str:
    return pathlib.Path("/".join(paths)).__str__().replace("\\", "/")


def merge_dir(src: pathlib.Path, dst: pathlib.Path, ignore_pattern: list[str]):
    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)

    for t in src.iterdir():

        dest = dst.joinpath(t.name)

        if t.is_dir():
            merge_dir(t, dest, ignore_pattern)
        else:
            if not any(regex_util.match_rules(ignore_pattern, t.as_posix()).values()):
                logger.debug(f"{t.as_posix()} => {dest.as_posix()}")
                file_util.copy(t, dest)
