#!/usr/bin/env python3
import filecmp

import pathlib
import shutil
import typing


def get_files(path: pathlib.Path, remove_prefix: str = "") -> list:
    return [a.as_posix().replace(remove_prefix, "") for a in path.rglob("*") if a.is_file()]


def read_text(file: pathlib.Path) -> str:
    try:
        return file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"file read error {file}: {e}")



def write_text(file: pathlib.Path, text: str, st_mode: int = None):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text, encoding="utf-8")
    if st_mode:
        file.chmod(st_mode)


def copy(src: pathlib.Path, dst: pathlib.Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)


# sync src files to dst; delete dst files by src not exist files
def sync(src: pathlib.Path, src_filter_func: typing.Callable[[pathlib.Path], bool], dst: pathlib.Path):
    # upsert
    for s in [a for a in src.rglob("*") if a.is_file()]:
        if src_filter_func(s):
            t = dst.joinpath(s.relative_to(src))
            if not t.exists() or not filecmp.cmp(s, t):
                copy(s, t)
    # delete
    for t in [a for a in dst.rglob("*") if a.is_file()]:
        s = src.joinpath(t.relative_to(dst))
        if not s.exists() or not src_filter_func(s):
            t.unlink(missing_ok=True)
