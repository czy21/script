#!/usr/bin/env python3


flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]


def arr_param_to_str(*items) -> str:
    return " ".join(flat(list(items)))
