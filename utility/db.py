#!/usr/bin/env python3
import io
import math
import os
import re
import subprocess

import jinja2
from colorama import Fore

from script.utility import path as path_util, basic as basic_util, log

logger = log.Logger(__name__)


def assemble_ql(s_path, t_file_name, db_meta, file_suffix, **kwargs) -> None:
    prep = kwargs.get("prep")
    post = kwargs.get("post")
    db_file_paths = path_util.dfs_dir(s_path, re.compile(r".*" + file_suffix))
    db_file_content = []
    for s in db_file_paths:
        logger.info(basic_util.action_formatter("loading", s, Fore.GREEN))
        with io.open(s, "r", encoding="utf-8") as cf:
            db_file_template = "\n".join([db_meta.self["header"], cf.read(), db_meta.self["footer"]])
            db_file_content.append(jinja2.Template(source=db_file_template).render(**{
                **{"file_path": s},
                **db_meta.self["substitution"]
            }))
    with io.open(t_file_name, "w", encoding="utf-8") as tf:
        if prep:
            db_file_content.insert(0, prep)
        if post:
            db_file_content.append(post)
        tf.write(u'{}'.format("\n".join(db_file_content)))


def print_ql_msg(msg_lines, proc: subprocess.Popen, func_param) -> None:
    exec_file_tuple = []
    for line in msg_lines:
        line = line.strip()
        if line:
            execute_match = re.compile(r"^\s*(executing:|executed:)").match(line)
            if execute_match:
                exec_file_tuple.append(line)
            if os.environ.run_args.debug:
                logger.debug(line, is_sleep=False)
            if not os.environ.run_args.debug and execute_match:
                logger.info(line)
    if math.modf(len(exec_file_tuple) / 2)[0] > 0:
        logger.error(str(exec_file_tuple[len(exec_file_tuple) - 1].strip()).replace("executing:", "error_file"))
