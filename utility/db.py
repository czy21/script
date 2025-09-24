#!/usr/bin/env python3
import io
import logging
import math
import pathlib
import re
import subprocess
import typing

import jinja2

from utility import basic as basic_util, path as path_util, file as file_util

logger = logging.getLogger()


def assemble_ql(s_path: pathlib.Path, t_file: pathlib.Path, db_meta: typing.Any, file_suffix: str, prep: str = None, post: str = None) -> None:
    db_file_paths = path_util.dfs_dir(s_path.as_posix(), re.compile(r".*" + file_suffix))
    db_file_content = []
    for s in db_file_paths:
        logger.info(basic_util.action_formatter("loading", s))
        with io.open(s, "r", encoding="utf-8") as cf:
            db_file_template = "\n".join([db_meta.self["header"], cf.read(), db_meta.self["footer"]])
            db_file_content.append(jinja2.Template(source=db_file_template).render(**{
                **{"file_path": s},
                **db_meta.self["substitution"]
            }))

    if prep:
        db_file_content.insert(0, prep)
    if post:
        db_file_content.append(post)

    file_util.write_text(t_file, u'{}'.format("\n\n".join(db_file_content)))


def print_ql_msg(msg_lines, proc: subprocess.Popen, func_param) -> None:
    exec_file_tuple = []
    for line in msg_lines:
        line = line.strip()
        if line:
            execute_match = re.compile(r"^\s*(executing:|executed:)").match(line)
            if execute_match:
                exec_file_tuple.append(line)
                logger.info(line)
    if math.modf(len(exec_file_tuple) / 2)[0] > 0:
        logger.error(str(exec_file_tuple[len(exec_file_tuple) - 1].strip()).replace("executing:", "exec_fail:"))