#!/usr/bin/env python3
import pathlib
from typing import NoReturn


def get_files(path: pathlib.Path, remove_prefix: str = "") -> list[str]:
    return [a.as_posix().replace(remove_prefix, "") for a in path.rglob("*") if a.is_file()]


def read_text(file: pathlib.Path) -> str:
    return file.read_text(encoding="utf-8")


def write_text(file: pathlib.Path, text: str) -> NoReturn:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text, encoding="utf-8")
