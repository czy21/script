import subprocess
import sys
from itertools import zip_longest
from pathlib import Path
from dotenv import dotenv_values

flat = lambda a: sum(map(flat, a), []) if isinstance(a, list) else [a]


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
    return 'echo "' + c + '"'


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


def execute(app_tuples, func, **kwargs):
    env_dict = dotenv_values(kwargs["env_file"]) if kwargs.__contains__("env_file") else {}
    param_iter = iter(kwargs["args"].p)
    param_input_dict = dict(zip(param_iter, param_iter))
    if param_input_dict:
        print(param_input_dict)
    env_dict.update(param_input_dict)
    for t in app_tuples:
        app_number = str(t[0])
        role_path = t[1]
        role_name = role_path.name
        role_title = ".".join([app_number, role_path.name])
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
