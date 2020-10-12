#!/usr/bin/env python3
import io
import math
import re

from colorama import Fore

from script.utility import path as path_util, basic as basic_util, log
from script.utility.template import CustomTemplate

logger = log.Logger(__name__)


def assemble_ql(s_path, t_file_name, db_meta, file_suffix) -> None:
    db_file_paths = path_util.dfs_dir(s_path, re.compile(r".*" + file_suffix))
    db_file_content = []
    for s in db_file_paths:
        logger.info(basic_util.action_formatter("loading", s, Fore.GREEN))
        header = CustomTemplate(text=db_meta.self["header"]).render(file_path=s)
        with io.open(s, "r", encoding="utf-8", newline="\n") as current_sql_file:
            content = CustomTemplate(current_sql_file.read()).render(**db_meta.self["substitution"])
        footer = CustomTemplate(text=db_meta.self["footer"]).render(file_path=s)
        db_file_content.append("\n".join([header, content, footer]))
    with io.open(t_file_name, "w+", encoding="utf-8", newline="\n") as t_file:
        t_file.write(u'{}'.format("\n\n".join(db_file_content)))


def print_ql_msg(msg_lines, *proc, **func_param) -> None:
    callback = list(filter(re.compile(r"^(executing:|executed:)").search, msg_lines))
    for m in callback[1::2]:
        logger.info(m.strip())
    if math.modf(len(callback) / 2)[0] > 0:
        logger.error(callback[len(callback) - 1].strip())
