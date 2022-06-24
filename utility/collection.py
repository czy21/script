#!/usr/bin/env python3


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
