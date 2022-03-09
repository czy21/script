#!/usr/bin/env python3


def flat(a): return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(items: list, delimiter=" ") -> str:
    return delimiter.join(flat(items))


def flat_dict(src, target=None, prefix=""):
    if target is None:
        target = {}
    for k, value in src.items():
        if isinstance(value, dict):
            flat_dict(value, target, prefix + k + "_")
        else:
            target[prefix + k] = value
    return target
