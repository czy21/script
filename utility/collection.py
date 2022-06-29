#!/usr/bin/env python3
import itertools

import jinja2
import pydash

from utility import template as template_util


def flat(a) -> list: return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(*items: list, delimiter: str = " ") -> str:
    return delimiter.join(flat(list(items)))


def flat_dict(data: dict) -> dict:
    ret = {}
    for k, v in data.items():
        if isinstance(v, list):
            ret.update(flat_dict({"{0}{1}".format(k, "[" + str(i) + "]"): t for i, t in enumerate(v)}))
        elif isinstance(v, dict):
            ret.update(flat_dict({"{0}.{1}".format(k, vk): vv for vk, vv in v.items()}))
        else:
            ret[k] = v
    return ret


def dict_render(data: dict) -> dict:
    for k, v in flat_dict(data).items():
        if isinstance(v, str):
            pydash.set_(data, k, template_util.Template(v).render(**data))
    return data


def print_grid(items: list, col_num: int = 0):
    rows = [list(t) for t in itertools.zip_longest(*[iter(items)] * col_num, fillvalue='')]
    col_lens = [len(max([t[p] for t in rows for p in range(col_num) if p == i], key=len, default='')) for i in range(col_num)]
    for t in rows:
        print("".join([str(t[p]).ljust(col_lens[o] + 2) for p in range(col_num) for o in range(col_num) if p == o]))
