# !/usr/bin/env python
import io
import math
import re

from colorama import init, Fore

from script.utility import path as path_util, template as template_util

init(autoreset=True)


def assemble_ql(s_path, t_file_name, db_meta, file_suffix, params):
    db_file_paths = path_util.dfs_dir(s_path, re.compile(r".*" + file_suffix))
    with io.open(t_file_name, "w+", encoding="utf-8", newline="\n") as t_file:
        for s in db_file_paths:
            header = template_util.StringTemplate(db_meta.self["header"])
            footer = template_util.StringTemplate(db_meta.self["footer"])
            print(Fore.GREEN + "loading => " + Fore.WHITE + s)
            t_file.write(u'{}'.format(header.safe_substitute(file_path=s) + "\n"))
            with io.open(s, "r", encoding="utf-8", newline="\n") as current_sql_file:
                t_file.write(template_util.StringTemplate(current_sql_file.read() + "\n")
                             .safe_substitute(dict(db_meta.self["substitution"])))
            t_file.write(u'{}'.format(footer.safe_substitute(file_path=s) + "\n\n"))


def filter_execution(iterator):
    return list(filter(re.compile(r"^(executing:|executed:)").search, iterator))


def print_msg(msg_lines):
    callback = filter_execution(msg_lines)
    for m in callback[1::2]:
        print(Fore.GREEN + m.replace("\n", ""))
    if math.modf(len(callback) / 2)[0] > 0:
        print(Fore.RED + callback[len(callback) - 1])


def print_cmd(class_name, method_name, command):
    print(Fore.CYAN + class_name + "_" + method_name + " => " + Fore.WHITE + command)
