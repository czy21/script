#!/usr/bin/env python3
import subprocess
import sys
from itertools import zip_longest
from pathlib import Path

flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]


def arr_param_to_str(*items, separator=" ") -> str:
    return separator.join(flat(list(items)))


def dfs_dir(target_path: Path, deep) -> list:
    ret = []
    for p in sorted(target_path.iterdir()):
        if p.is_dir():
            ret.append({"path": p, "deep": deep})
            ret += dfs_dir(p, deep + 1)
    return ret


def get_install_tuple(root_path: Path):
    app_paths = [p for p in sorted(root_path.iterdir()) if p.is_dir()]
    # group by
    list_str = [list(t) for t in zip_longest(*[iter([".".join([str(i), p.name]) for i, p in enumerate(app_paths, start=1)])] * 8, fillvalue='')]
    # get every column max length
    column_widths = [len(max([t[p] for t in list_str for p in range(len(t)) if p == i], key=len, default='')) for i in range(len(list_str[0]))]
    for t in list_str:
        print("".join([str(t[p]).ljust(column_widths[o] + 2) for p in range(len(t)) for o in range(len(column_widths)) if p == o]))
    app_options = input("please select app number(example:1 2 3) ").strip().split()
    return [(int(t), app_paths.__getitem__(int(t) - 1)) for t in app_options if t in [str(i) for i, p in enumerate(app_paths, start=1)]]


def select_option(deep):
    deep_index = 1
    flat_dirs = dfs_dir(Path(__file__).parent, deep_index)

    path = None

    while deep > deep_index:
        o = []
        for t in flat_dirs:
            if deep_index == t["deep"]:
                if path is None:
                    o.append(t["path"])
                else:
                    if str(t["path"].as_posix()).startswith(path.as_posix()):
                        o.append(t["path"])
        for i, p in enumerate(o, start=1):
            print(" ".join([str(i), p.name]))
        one_option = input("please select one option(example:1) ").strip()
        if one_option == '':
            sys.exit()
        if not one_option.isnumeric():
            print("\ninvalid option")
            sys.exit()
        one_option = int(one_option)
        if one_option not in [i for i, p in enumerate(o, start=1)]:
            print(" ".join(["\n", one_option, "not exist"]))
            sys.exit()
        path = o[one_option - 1]
        deep_index = deep_index + 1
    return {
        "namespace": path.name,
        "list": get_install_tuple(path)
    }


def execute_cmd(cmd: str):
    proc = subprocess.Popen(cmd, shell=True, encoding="utf-8")
    proc.wait()
