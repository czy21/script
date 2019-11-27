# !/usr/bin/env python
import os
import re


def dfs_dir(target_path, pattern=None):
    ret = []
    sort_target = os.listdir(target_path)
    sort_target.sort(key=lambda x: re.compile("^\\d+").match(x).group() if re.compile("^\\d+").match(x) else x)
    for sub_p in sort_target:
        tmp_path = join(target_path, sub_p)
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


def join(path, *paths):
    return os.path.join(path, *paths).replace('\\', '/').strip()
