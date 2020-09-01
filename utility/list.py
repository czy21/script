#!/usr/bin/env python3


def arr_param_to_str(*items) -> str:
    return " ".join(["", " ".join([x for tup in items for x in tup]), ""])
