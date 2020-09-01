#!/usr/bin/env python3
import os
import re
from pathlib import Path


def dfs_dir(target_path, pattern=None) -> list:
    ret = []
    sort_target = os.listdir(target_path)
    sort_target.sort(key=lambda x: re.compile("^\\d+").match(x).group() if re.compile("^\\d+").match(x) else x)
    for sub_p in sort_target:
        tmp_path = os_path_join(target_path, sub_p)
        if os.path.isfile(tmp_path):
            if pattern:
                match = pattern.match(tmp_path)
                if match:
                    ret.append(match.group())
            else:
                ret.append(tmp_path)
        elif os.path.isdir(tmp_path):
            ret += dfs_dir(tmp_path)
    return ret


def os_path_join(path, *paths) -> str:
    return os.path.join(path, *paths).replace('\\', '/').strip()


def pure_path_join(root, *elements) -> str:
    left_path = Path(root).resolve()
    for p in elements:
        left_path = left_path.joinpath(p)
    return left_path.as_posix()
