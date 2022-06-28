#!/usr/bin/env python3
import itertools


def flat(a) -> list: return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(*items: list, delimiter: str = " ") -> str:
    return delimiter.join(flat(list(items)))


def flat_dict(src, target=None, prefix=""):
    if target is None:
        target = {}
    for k, value in src.items():
        if isinstance(value, dict):
            flat_dict(value, target, prefix + k + "_")
        else:
            target[prefix + k] = value
    return target


def print_grid(items: list, col_num: int = 0):
    rows = [list(t) for t in itertools.zip_longest(*[iter(items)] * col_num, fillvalue='')]
    col_lens = [len(max([t[p] for t in rows for p in range(col_num) if p == i], key=len, default='')) for i in range(col_num)]
    for t in rows:
        print("".join([str(t[p]).ljust(col_lens[o] + 2) for p in range(col_num) for o in range(col_num) if p == o]))
