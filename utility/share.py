import subprocess
import sys
from itertools import zip_longest
from pathlib import Path
from dotenv import dotenv_values

flat = lambda a: sum(map(flat, a), []) if isinstance(a, list) else [a]


def arr_param_to_str(*items, separator=" ") -> str:
    return separator.join(flat(list(items)))


def dfs_dir(target_path: Path, deep=1) -> list:
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
    return 'echo "' + c + '"'


def get_install_tuple(app_path: Path) -> dict:
    app_dict: dict = {str(i): t for i, t in enumerate([p for p in sorted(app_path.iterdir()) if p.is_dir()], start=1)}
    # group by
    col_group = [list(t) for t in zip_longest(*[iter([".".join([str(k), v.name]) for k, v in app_dict.items()])] * 5, fillvalue='')]
    # get every column max length
    col_widths = [len(max([t[p] for t in col_group for p in range(len(t)) if p == i], key=len, default='')) for i in range(len(col_group[0]))]
    for t in col_group:
        print("".join([str(t[p]).ljust(col_widths[o] + 2) for p in range(len(t)) for o in range(len(col_widths)) if p == o]))
    app_nums = input("please select app number(example:1 2 3) ").strip().split()
    return dict((t, app_dict[t]) for t in app_nums if t in app_dict.keys())


def select_option(deep: int = 1) -> dict:
    root_path = Path(__file__).parent
    flat_dirs = dfs_dir(root_path)
    app_path = root_path
    deep_index = 1

    while deep > deep_index:
        app_dict = {str(i): p for i, p in enumerate(map(lambda a: a["path"], filter(lambda a: a["deep"] == deep_index, flat_dirs)), start=1)}
        for k, v in app_dict.items():
            print(" ".join([k, v.name]))
        one_option = input("please select one option(example:1) ").strip()
        if one_option == '':
            sys.exit()
        if not one_option.isnumeric():
            print("\ninvalid option")
            sys.exit()
        if one_option not in app_dict.keys():
            print(" ".join(["\n", str(one_option), "not exist"]))
            sys.exit()
        app_path = app_dict[one_option]
        deep_index = deep_index + 1
    return {
        "namespace": app_path.name,
        "list": get_install_tuple(app_path)
    }


def execute_cmd(cmd):
    subprocess.Popen(cmd, shell=True).wait()


def execute(app_dict, func, **kwargs):
    env_dict = dotenv_values(kwargs["env_file"]) if kwargs.__contains__("env_file") else {}
    param_iter = iter(kwargs["args"].p)
    param_input_dict = dict(zip(param_iter, param_iter))
    if param_input_dict:
        print(param_input_dict)
    env_dict.update(param_input_dict)
    for t in app_dict.items():
        app_num = t[0]
        role_path = t[1]
        role_name = role_path.name
        role_title = ".".join([app_num, role_path.name])
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
