#!/usr/bin/env python3
import itertools
import logging
import typing

logger = logging.getLogger()


def flat(a) -> list: return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(*items: typing.Any, delimiter: str = " ") -> str:
    return delimiter.join(flat(list(items)))


def flat_dict(source: dict):
    result = {}
    _build_flat_dict(result, source, None)
    return result


def _build_flat_dict(result: dict, source: dict, path):
    for key, value in source.items():
        if path is not None and str.strip(path).__len__() > 0:
            if key.startswith("["):
                key = path + key
            else:
                key = path + "." + key
        if isinstance(value, str):
            result[key] = value
        elif isinstance(value, dict):
            _build_flat_dict(result, value, key)
        elif isinstance(value, list):
            if not value:
                result[key] = ""
            else:
                count = 0
                for obj in value:
                    _build_flat_dict(result, {'[{}]'.format(count): obj}, key)
                    count += 1
        else:
            result[key] = value if value else ""


def print_grid(items: list, col_num: int = 0, msg: str = ""):
    rows = [list(t) for t in itertools.zip_longest(*[iter(items)] * col_num, fillvalue='')]
    col_lens = [len(max([t[p] for t in rows for p in range(col_num) if p == i], key=len, default='')) for i in range(col_num)]
    logger.info(msg + "\n".join(["", *["".join([str(t[p]).ljust(col_lens[o] + 2) for p in range(col_num) for o in range(col_num) if p == o]) for t in rows]]))
