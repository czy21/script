# !/usr/bin/env python


def arr_param_to_str(*items):
    arr = []
    for t in items:
        arr[len(arr):len(arr)] = t
    return " ".join(["", " ".join(arr), ""])
