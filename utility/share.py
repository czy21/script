#!/usr/bin/env python3
import sys
from itertools import zip_longest
from pathlib import Path


def get_install_tuple(join_path):
    app_paths = [p for p in sorted(Path(__file__).parent.joinpath(join_path).iterdir()) if p.is_dir()]
    # group by
    list_str = [list(t) for t in zip_longest(*[iter([".".join([str(i), p.name]) for i, p in enumerate(app_paths, start=1)])] * 8, fillvalue='')]
    # get every column max length
    column_widths = [len(max([t[p] for t in list_str for p in range(len(t)) if p == i], key=len, default='')) for i in range(len(list_str[0]))]
    for t in list_str:
        print("".join([str(t[p]).ljust(column_widths[o] + 2) for p in range(len(t)) for o in range(len(column_widths)) if p == o]))
    app_options = input("please select app number(example:1 2 3) ").strip().split()
    return [(int(t), app_paths.__getitem__(int(t) - 1)) for t in app_options if t in [str(i) for i, p in enumerate(app_paths, start=1)]]


def select_one_option():
    list_dir = [p for p in sorted(Path(__file__).parent.iterdir()) if p.is_dir()]

    print("\n==========")

    for i, p in enumerate(list_dir, start=1):
        print(" ".join([str(i), p.name]))

    one_option = input("please select one option(example:1) ").strip()

    if one_option == '':
        sys.exit()

    if not one_option.isnumeric():
        print("\ninvalid option")
        sys.exit()

    one_option = int(one_option)

    if one_option not in [i for i, p in enumerate(list_dir, start=1)]:
        print(" ".join(["\n", one_option, "not exist"]))
        sys.exit()
    return list_dir[one_option - 1]
