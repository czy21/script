#!/usr/bin/env python3
import itertools
import logging
import typing

logger = logging.getLogger()


def flat(a) -> list: return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(*items: typing.Any, delimiter: str = " ") -> str:
    return delimiter.join(flat(list(items)))


def flat_dict(
        source: dict,
        key_wrap_func: typing.Callable[[str], str] = lambda k: '.' + k,
        val_predicate: typing.Callable[[typing.Any], bool] = lambda v: True,
        value_empty: typing.Literal["origin", "", None] = "origin"
) -> dict:
    result = {}
    _build_flat_dict(result, source, None, key_wrap_func, val_predicate, value_empty)
    return result


def _build_flat_dict(
        result: dict,
        source: dict,
        path: typing.Union[str, None],
        key_wrap_func: typing.Callable[[str], str],
        val_predicate: typing.Callable[[typing.Any], bool],
        value_empty: typing.Literal["origin", "", None]
):
    for key, value in source.items():
        if path and str.strip(path):
            key = path + (key if key.startswith("[") else key_wrap_func(key))
        if isinstance(value, str):
            if val_predicate(value):
                result[key] = value
        elif isinstance(value, dict):
            if not value and val_predicate(value):
                result[key] = value if value_empty == "origin" else value_empty
            _build_flat_dict(result, value, key, key_wrap_func, val_predicate, value_empty)
        elif isinstance(value, list):
            if not value and val_predicate(value):
                result[key] = value if value_empty == "origin" else value_empty
            else:
                count = 0
                for obj in value:
                    _build_flat_dict(result, {'[{}]'.format(count): obj}, key, key_wrap_func, val_predicate, value_empty)
                    count += 1
        else:
            if val_predicate(value):
                result[key] = value if value_empty == "origin" else value_empty


def print_grid(items: list, col_num: int = 0, msg: str = ""):
    rows = [list(t) for t in itertools.zip_longest(*[iter(items)] * col_num, fillvalue='')]
    col_lens = [len(max([t[p] for t in rows for p in range(col_num) if p == i], key=len, default='')) for i in range(col_num)]
    logger.info(msg + "\n".join(["", *["".join([str(t[p]).ljust(col_lens[o] + 2) for p in range(col_num) for o in range(col_num) if p == o]) for t in rows]]))
