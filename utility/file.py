#!/usr/bin/env python3
import base64
import pathlib


def read_file(file: pathlib.Path, read_func):
    with open(file, mode="r", encoding="utf-8") as f:
        return read_func(f)


def write_file(file: pathlib.Path, write_func, mode: str = "w"):
    with open(file, mode=mode, encoding="utf-8") as f:
        write_func(f)


def yaml_join_tag(loader, node):
    return "".join(loader.construct_sequence(node, deep=True))


def yaml_decode_tag(loader, node):
    decode_args = loader.construct_sequence(node, deep=True)
    decode_way = decode_args[0]
    encode_val = decode_args[1]
    if decode_way == "base64":
        return base64.b64decode(encode_val).rstrip().decode("utf-8")
    return encode_val


def get_files(path: pathlib.Path, remove_prefix: str = ""):
    return [a.as_posix().replace(remove_prefix, "") for a in path.rglob("*") if a.is_file()]
