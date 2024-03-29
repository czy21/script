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
    resources: dict[pathlib.Path, pathlib.Path] = {
        r: dst.joinpath(r.relative_to(src))
        for r in src.rglob("*")
        if not any(regex_util.match_rules(ignore_pattern, r.as_posix()).values())
    }
    for k, v in resources.items():
        if k.is_dir():
            v.mkdir(parents=True, exist_ok=True)
        elif k.is_file() and not v.exists():
            file_util.copy(k, v)
