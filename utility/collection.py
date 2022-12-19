#!/usr/bin/env python3
import itertools
import logging
import typing

import pydash

import template

logger = logging.getLogger()


def flat(a) -> list: return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(*items: typing.Any, delimiter: str = " ") -> str:
    return delimiter.join(flat(list(items)))


def flat_dict(data: dict) -> dict:
    ret = {}
    for k, v in data.items():
        if isinstance(v, list):
            ret |= flat_dict({"{0}{1}".format(k, "[" + str(i) + "]"): t for i, t in enumerate(v)})
        elif isinstance(v, dict):
            ret |= flat_dict({"{0}.{1}".format(k, vk): vv for vk, vv in v.items()})
        else:
            ret[k] = v
    return ret


def dict_render(data: dict) -> dict:
    d = data.copy()
    for k, v in flat_dict(d).items():
        if isinstance(v, str) and v.__contains__("{{"):
            pydash.set_(d, k, template.Template(v).render(**d))
    return d


def print_grid(items: list, col_num: int = 0, msg: str = ""):
    rows = [list(t) for t in itertools.zip_longest(*[iter(items)] * col_num, fillvalue='')]
    col_lens = [len(max([t[p] for t in rows for p in range(col_num) if p == i], key=len, default='')) for i in range(col_num)]
    logger.info(msg + "\n".join(["", *["".join([str(t[p]).ljust(col_lens[o] + 2) for p in range(col_num) for o in range(col_num) if p == o]) for t in rows]]))
