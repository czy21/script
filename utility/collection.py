#!/usr/bin/env python3


flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]


def arr_param_to_str(*items) -> str:
    return " ".join(flat(list(items)))


def flat_dict(src, target=None, prefix=""):
    if target is None:
        target = {}
    for k, value in src.items():
        if isinstance(value, dict):
            flat_dict(value, target, prefix + k + ".")
        else:
            target[prefix + k] = value
    return target
