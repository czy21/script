#!/usr/bin/env python3
import pathlib
from typing import Callable, Any, TextIO, NoReturn


def get_files(path: pathlib.Path, remove_prefix: str = "") -> list[str]:
    return [a.as_posix().replace(remove_prefix, "") for a in path.rglob("*") if a.is_file()]


def read_file(file: pathlib.Path, read_func: Callable[[TextIO], Any]) -> Any:
    with open(file, mode="r", encoding="utf-8") as f:
        return read_func(f)


def write_file(file: pathlib.Path, write_func: Callable[[TextIO], NoReturn], mode: str = "w") -> NoReturn:
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, mode=mode, encoding="utf-8") as f:
        write_func(f)
