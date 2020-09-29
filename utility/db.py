#!/usr/bin/env python3
import io
import math
import re

from colorama import Fore

from script.utility import path as path_util, template as template_util, basic as basic_util, logging

logger = logging.Logger(__name__)


def assemble_ql(s_path, t_file_name, db_meta, file_suffix) -> None:
    db_file_paths = path_util.dfs_dir(s_path, re.compile(r".*" + file_suffix))
    with io.open(t_file_name, "w+", encoding="utf-8", newline="\n") as t_file:
        for s in db_file_paths:
            header = template_util.StringTemplate(db_meta.self["header"])
            footer = template_util.StringTemplate(db_meta.self["footer"])
            logger.info(basic_util.action_formatter("loading", s, Fore.GREEN))
            t_file.write(u'{}'.format(header.safe_substitute(file_path=s) + "\n"))
            with io.open(s, "r", encoding="utf-8", newline="\n") as current_sql_file:
                t_file.write(template_util.StringTemplate(current_sql_file.read() + "\n")
                             .safe_substitute(dict(db_meta.self["substitution"])))
            t_file.write(u'{}'.format(footer.safe_substitute(file_path=s) + "\n\n"))


def filter_execution(iterator) -> list:
    return list(filter(re.compile(r"^(executing:|executed:)").search, iterator))


def print_ql_msg(msg_lines) -> None:
    callback = filter_execution(msg_lines)
    for m in callback[1::2]:
        logger.info(Fore.WHITE + m.replace("\n", ""))
    if math.modf(len(callback) / 2)[0] > 0:
        logger.info(Fore.RED + callback[len(callback) - 1])
