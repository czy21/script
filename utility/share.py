import itertools
import pathlib
import re
import subprocess
import sys

import dotenv


def flat(a): return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(*items: list, delimiter=" ") -> str:
    return delimiter.join(flat(list(items)))


def exclude_match(pattern, name):
    return pattern is None or not re.search(pattern, name)


def dfs_dir(path: pathlib.Path, deep=1, exclude_pattern: str = None) -> list:
    ret = []
    for p in filter(lambda a: a.is_dir() and exclude_match(exclude_pattern, a.as_posix()), sorted(path.iterdir())):
        ret.append({"path": p, "deep": deep})
        ret += dfs_dir(p, deep + 1, exclude_pattern)
    return ret


def role_print(role, content, exec_file=None) -> str:
    c = "{}\033[32m {} \033[0m".format(role, content)
    if exec_file:
        c += "=> {}".format(exec_file)
    return 'echo "' + c + '"'


def get_dir_dict(root_path: pathlib.Path, exclude_pattern=None, select_tip="") -> dict:
    role_dict: dict = {str(i): t for i, t in enumerate(filter(lambda a: a.is_dir() and exclude_match(exclude_pattern, a.as_posix()), sorted(root_path.iterdir())), start=1)}
    # group by
    col_group = [list(t) for t in itertools.zip_longest(*[iter([".".join([str(k), v.name]) for k, v in role_dict.items()])] * 5, fillvalue='')]
    # get every column max length
    col_widths = [len(max([t[p] for t in col_group for p in range(len(t)) if p == i], key=len, default='')) for i in range(len(col_group[0]))]
    for t in col_group:
        print("".join([str(t[p]).ljust(col_widths[o] + 2) for p in range(len(t)) for o in range(len(col_widths)) if p == o]))
    role_nums = input("please select {0}".format(select_tip)).strip().split()
    return dict((t, role_dict[t]) for t in role_nums if t in role_dict.keys())


def select_option(deep: int = 1, exclude_path=None) -> dict:
    if exclude_path is None:
        exclude_path = []
    exclude_path.append("___temp")
    exclude_pattern = "({0})".format("|").join(set(exclude_path))
    root_path = pathlib.Path(__file__).parent
    flat_dirs = dfs_dir(root_path, exclude_pattern=exclude_pattern)

    app_path = root_path
    deep_index = 1

    while deep > deep_index:
        role_dict = {str(i): p for i, p in enumerate(map(lambda a: a["path"], filter(lambda a: a["deep"] == deep_index, flat_dirs)), start=1)}
        for k, v in role_dict.items():
            print(" ".join([k, v.name]))
        selected = input("please select one option(example:1) ").strip()
        if selected == '':
            sys.exit()
        if selected not in role_dict.keys():
            print(" ".join(["\n", str(selected), "not exist"]))
            sys.exit()
        app_path = role_dict[selected]
        deep_index = deep_index + 1
    return {
        "namespace": app_path.name,
        "role_dict": get_dir_dict(app_path, exclude_pattern=exclude_pattern, select_tip="role num(example:1 2 3)"),
        "exclude_pattern": exclude_pattern
    }


def execute_cmd(cmd):
    # print(cmd)
    subprocess.Popen(cmd, shell=True).wait()


def execute(ctx, func, **kwargs):
    kwargs["args"].exclude_pattern = ctx["exclude_pattern"]
    env_dict = dotenv.dotenv_values(kwargs["env_file"]) if kwargs.__contains__("env_file") else {}
    param_iter = iter(kwargs["args"].p)
    param_input_dict = dict(zip(param_iter, param_iter))
    if param_input_dict:
        print(param_input_dict)
    env_dict.update(param_input_dict)
    for t in ctx["role_dict"].items():
        role_num = t[0]
        role_path = t[1]
        role_name = role_path.name
        role_title = ".".join([role_num, role_path.name])
        func(role_title=role_title,
             role_path=role_path,
             env_dict={
                 **env_dict,
                 **{
                     "param_role_name": role_name,
                     "param_role_path": role_path.as_posix(),
                     "param_role_title": role_title
                 }
             },
             **kwargs)
