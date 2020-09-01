#!/usr/bin/env python3


def arr_param_to_str(*items):
    arr = []
    for t in items:
        arr[len(arr):len(arr)] = t
    return " ".join(["", " ".join(arr), ""])
