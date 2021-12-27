#!/usr/bin/env python3
import re
import subprocess
import sys
from itertools import zip_longest
from pathlib import Path

import mako.lexer
import mako.template
import mako.parsetree

flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]


class LexerCls(mako.lexer.Lexer):
    def match_expression(self):
        match = self.match(r"\{{")
        if match:
            line, pos = self.matched_lineno, self.matched_charpos
            text, end = self.parse_until_text(True, r"\|", r"}}")
            if end == "|":
                escapes, end = self.parse_until_text(True, r"}}")
            else:
                escapes = ""
            text = text.replace("\r\n", "\n")
            self.append_node(
                mako.parsetree.Expression,
                text,
                escapes.strip(),
                lineno=line,
                pos=pos,
            )
            return True
        else:
            return False

    def match_text(self):
        match = self.match(
            r"""
                (.*?)         # anything, followed by:
                (
                 (?=\{{)      # an expression
                 |
                 \Z           # end of string
                )""",
            re.X | re.S,
        )

        if match:
            text = match.group(1)
            if text:
                self.append_node(mako.parsetree.Text, text)
            return True
        else:
            return False


class Template(mako.template.Template):
    lexer_cls = LexerCls

    def __init__(self, text=None, filename=None, strict_undefined=True):
        mako.template.Template.__init__(self, text=text, filename=filename, strict_undefined=strict_undefined)


def arr_param_to_str(*items, separator=" ") -> str:
    return separator.join(flat(list(items)))


def dfs_dir(target_path: Path, deep) -> list:
    ret = []
    for p in sorted(target_path.iterdir()):
        if p.is_dir():
            ret.append({"path": p, "deep": deep})
            ret += dfs_dir(p, deep + 1)
    return ret


def role_print(role, content, exec_file=None) -> str:
    c = "{}\033[32m {} \033[0m".format(role, content)
    if exec_file:
        c += "=> {}".format(exec_file)
    return 'echo -e "' + c + '"'


def get_install_tuple(root_path: Path) -> list:
    app_paths = [p for p in sorted(root_path.iterdir()) if p.is_dir()]
    # group by
    list_str = [list(t) for t in zip_longest(*[iter([".".join([str(i), p.name]) for i, p in enumerate(app_paths, start=1)])] * 5, fillvalue='')]
    # get every column max length
    column_widths = [len(max([t[p] for t in list_str for p in range(len(t)) if p == i], key=len, default='')) for i in range(len(list_str[0]))]
    for t in list_str:
        print("".join([str(t[p]).ljust(column_widths[o] + 2) for p in range(len(t)) for o in range(len(column_widths)) if p == o]))
    app_options = input("please select app number(example:1 2 3) ").strip().split()
    return [(int(t), app_paths.__getitem__(int(t) - 1)) for t in app_options if t in [str(i) for i, p in enumerate(app_paths, start=1)]]


def select_option(deep) -> dict:
    deep_index = 1
    flat_dirs = dfs_dir(Path(__file__).parent, deep_index)

    path = None

    while deep > deep_index:
        o = []
        for t in flat_dirs:
            if deep_index == t["deep"]:
                if path is None:
                    o.append(t["path"])
                else:
                    if str(t["path"].as_posix()).startswith(path.as_posix()):
                        o.append(t["path"])
        for i, p in enumerate(o, start=1):
            print(" ".join([str(i), p.name]))
        one_option = input("please select one option(example:1) ").strip()
        if one_option == '':
            sys.exit()
        if not one_option.isnumeric():
            print("\ninvalid option")
            sys.exit()
        one_option = int(one_option)
        if one_option not in [i for i, p in enumerate(o, start=1)]:
            print(" ".join(["\n", one_option, "not exist"]))
            sys.exit()
        path = o[one_option - 1]
        deep_index = deep_index + 1
    return {
        "namespace": path.name,
        "list": get_install_tuple(path)
    }


def execute_cmd(cmd):
    subprocess.Popen(cmd, shell=True).wait()
