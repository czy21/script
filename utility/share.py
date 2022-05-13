import argparse
import itertools
import pathlib
import re
import subprocess
import sys

import jinja2
import yaml


def flat(a): return sum(map(flat, a), []) if isinstance(a, list) else [a]


def flat_to_str(*items: list, delimiter=" ") -> str:
    return delimiter.join(flat(list(items)))


def exclude_match(pattern, name):
    return pattern is None or not bool(re.search(pattern, name))


def read_file(file: pathlib.Path, read_func):
    with open(file, mode="r", encoding="utf-8") as f:
        return read_func(f)


def write_file(file: pathlib.Path, write_func, mode: str = "w"):
    with open(file, mode=mode, encoding="utf-8") as f:
        write_func(f)


def dfs_dir(path: pathlib.Path, deep=1, exclude_pattern: str = None) -> list:
    ret = []
    for p in filter(lambda a: a.is_dir() and exclude_match(exclude_pattern, a.as_posix()), sorted(path.iterdir())):
        ret.append({"path": p, "deep": deep})
        ret += dfs_dir(p, deep + 1, exclude_pattern)
    return ret


def get_files(path: pathlib.Path, remove_prefix: str = ""):
    return [a.as_posix().replace(remove_prefix, "") for a in path.rglob("*") if a.is_file()]


def role_print(role, content, exec_file=None) -> str:
    c = "{}\033[32m {} \033[0m".format(role, content)
    if exec_file:
        c += "=> {}".format(exec_file)
    return 'echo "' + c + '"'


def get_dir_dict(root_path: pathlib.Path, exclude_pattern=None, select_tip="", col_num=5) -> dict:
    dir_dict: dict = {str(i): t for i, t in enumerate(filter(lambda a: a.is_dir() and exclude_match(exclude_pattern, a.as_posix()), sorted(root_path.iterdir())), start=1)}
    col_rows = [list(t) for t in itertools.zip_longest(*[iter(["{0}.{1}".format(str(k), v.name) for k, v in dir_dict.items()])] * col_num, fillvalue='')]
    # get every col max len
    col_lens = [len(max([t[p] for t in col_rows for p in range(col_num) if p == i], key=len, default='')) for i in range(col_num)]
    for t in col_rows:
        print("".join([str(t[p]).ljust(col_lens[o] + 2) for p in range(col_num) for o in range(col_num) if p == o]))
    dir_nums = input("please select {0}:".format(select_tip)).strip().split()
    return dict((t, dir_dict[t]) for t in dir_nums if t in dir_dict.keys())


def select_option(deep: int = 1, excludes=None) -> dict:
    if excludes is None:
        excludes = []
    excludes.append("___temp")
    exclude_pattern = "({0})".format("|").join(set(excludes))
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
        "excludes": excludes
    }


def run_cmd(cmd):
    # print(cmd)
    subprocess.Popen(cmd, shell=True).wait()


def loop_role_dict(role_dict: dict,
                   role_func,
                   env_dict,
                   jinja2ignore_rules: list,
                   **kwargs):
    for k, v in role_dict.items():
        role_num = k
        role_path = v
        role_name = role_path.name
        role_title = ".".join([role_num, role_name])

        role_env_dict = {
            **env_dict,
            **{
                "param_role_name": role_name,
                "param_role_path": role_path.as_posix(),
                "param_role_title": role_title
            }
        }
        # parse jinja2 template
        for t in filter(lambda f: f.is_file(), role_path.rglob("*")):
            _exclude_bools = [exclude_match(r, t.as_posix()) for r in jinja2ignore_rules]
            if all(_exclude_bools):
                template_value = read_file(t, lambda f: jinja2.Template(f.read()).render(**role_env_dict))
                write_file(t, lambda f: f.write(template_value))
        role_func(role_title=role_title, role_path=role_path, role_env_dict=role_env_dict, **kwargs)


class Installer:
    def __init__(self,
                 root_path: pathlib.Path,
                 role_func,
                 role_deep: int = 1
                 ) -> None:
        self.root_path: pathlib.Path = root_path
        self.bak_path: pathlib.Path = root_path.joinpath("___temp/bak")
        self.env_file: pathlib.Path = root_path.joinpath("env.yaml")
        self.jinja2ignore_file: pathlib.Path = root_path.joinpath(".jinja2ignore")
        self.role_func = role_func
        self.role_deep: int = role_deep
        self.arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()

    def run(self, **kwargs):
        yaml.add_constructor('!join', lambda loader, node: "".join(loader.construct_sequence(node, deep=True)))
        self.arg_parser.add_argument('-p', '--param', nargs="+", default=[])
        self.arg_parser.add_argument('-i', '--install', action="store_true")
        self.arg_parser.add_argument('-d', '--delete', action="store_true")
        self.arg_parser.add_argument('-b', '--build-file', type=str)
        self.arg_parser.add_argument('-a', '--action', type=str, required=False)
        self.arg_parser.add_argument('-n', '--namespace')
        self.arg_parser.add_argument('--debug', action="store_true")

        args: argparse.Namespace = self.arg_parser.parse_args()

        # select role
        selected_dict = select_option(self.role_deep)
        selected_role_dict = selected_dict["role_dict"]
        selected_role_namespace = selected_dict["namespace"]
        if args.namespace is None:
            args.namespace = selected_role_namespace

        global_env_dict = {}
        # read env_file
        if self.env_file and self.env_file.exists():
            global_env_dict.update(read_file(self.env_file, lambda f: yaml.full_load(f)))
        # read input param
        param_input_iter = iter(args.param)
        param_input_dict = dict(zip(param_input_iter, param_input_iter))
        global_env_dict.update(param_input_dict)
        # global env_dict finished
        global_jinja2ignore_rules = []
        if self.jinja2ignore_file and self.jinja2ignore_file.exists():
            global_jinja2ignore_rules = read_file(self.jinja2ignore_file, lambda f: [t.strip("\n") for t in f.readlines()])
        # loop selected_role_dict
        loop_role_dict(
            role_dict=selected_role_dict,
            role_func=self.role_func,
            env_dict=global_env_dict,
            jinja2ignore_rules=global_jinja2ignore_rules,
            args=args,
            **kwargs
        )
