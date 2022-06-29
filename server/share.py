import argparse
import json
import logging
import pathlib
import subprocess
import sys

from utility import collection as collection_util, file as file_util, regex as regex_util, template as template_util, yaml as yaml_util, log as log_util

logger = logging.getLogger()


def dfs_dir(path: pathlib.Path, deep=1, exclude_rules: list = None) -> list:
    ret = []
    all_dirs = list(filter(lambda a: a.is_dir(), sorted(path.iterdir())))
    _include_dirs = []
    for p in all_dirs:
        _rules = regex_util.match_rules(exclude_rules, p.as_posix(), ".jinia2ignore {0}".format(dfs_dir.__name__))
        if not any([r["isMatch"] for r in _rules]):
            _include_dirs.append(p)
    for p in _include_dirs:
        ret.append({"path": p, "deep": deep})
        ret += dfs_dir(p, deep + 1, exclude_rules)
    return ret


def role_print(role, content, exec_file=None) -> str:
    c = "{}\033[32m {} \033[0m".format(role, content)
    if exec_file:
        c += "=> {}".format(exec_file)
    return 'echo "' + c + '"'


def get_dir_dict(root_path: pathlib.Path, exclude_rules: list = None, select_tip="", col_num=5) -> dict:
    all_dirs = list(filter(lambda a: a.is_dir(), sorted(root_path.iterdir())))
    _include_dirs = []
    for p in all_dirs:
        _rules = regex_util.match_rules(exclude_rules, p.as_posix(), ".jinia2ignore {0}".format(get_dir_dict.__name__))
        if not any([r["isMatch"] for r in _rules]):
            _include_dirs.append(p)
    dir_dict: dict = {str(i): t for i, t in enumerate(_include_dirs, start=1)}
    collection_util.print_grid(["{0}.{1}".format(str(k), v.name) for k, v in dir_dict.items()], col_num=col_num)
    dir_nums = input("please select {0}:".format(select_tip)).strip().split()
    return dict((t, dir_dict[t]) for t in dir_nums if t in dir_dict.keys())


def select_option(root_path: pathlib.Path, deep: int = 1, exclude_rules=None, args: argparse.Namespace = None):
    exclude_rules = exclude_rules if exclude_rules is not None else []
    exclude_rules.extend(["___temp", "utility"])
    flat_dirs = dfs_dir(root_path, exclude_rules=exclude_rules)

    app_path = root_path
    deep_index = 1

    while deep > deep_index:
        role_dict = {str(i): p for i, p in enumerate(map(lambda a: a["path"], filter(lambda a: a["deep"] == deep_index, flat_dirs)), start=1)}
        collection_util.print_grid(["{0}.{1}".format(k, v.name) for k, v in role_dict.items()], col_num=5)
        selected = input("please select one option(example:1) ").strip()
        if selected == '':
            sys.exit()
        if selected not in role_dict.keys():
            logger.error(" ".join(["\n", str(selected), "not exist"]))
            sys.exit()
        app_path = role_dict[selected]
        deep_index = deep_index + 1
    if args.namespace is None:
        args.namespace = app_path.name
    return get_dir_dict(app_path, exclude_rules=exclude_rules, select_tip="role num(example:1 2 3)"), exclude_rules


def run_cmd(cmd):
    logger.debug(cmd)
    subprocess.Popen(cmd, shell=True).wait()


def loop_role_dict(role_dict: dict,
                   role_func,
                   global_env,
                   args: argparse.Namespace,
                   jinja2ignore_rules: list,
                   **kwargs):
    for k, v in role_dict.items():
        role_num = k
        role_path: pathlib.Path = v
        role_name = role_path.name
        role_title = ".".join([role_num, role_name])
        role_env_file = role_path.joinpath("env.yaml")
        role_env = {
            **global_env,
            **{
                "param_role_name": role_name,
                "param_role_path": role_path.as_posix(),
                "param_role_title": role_title
            }
        }
        if role_env_file and role_env_file.exists():
            role_env.update(yaml_util.load(file_util.read_file(role_env_file, lambda f: template_util.Template(f.read()).render(**role_env))))
        logger.debug("{0} params: {1}".format(role_name, json.dumps(role_env, indent=1)))
        # parse jinja2 template
        for t in filter(lambda f: f.is_file(), role_path.rglob("*")):
            _rules = regex_util.match_rules([*jinja2ignore_rules, *["var/.*.yaml"]], t.as_posix(), ".jinia2ignore {0}".format(loop_role_dict.__name__))
            if not any([r["isMatch"] for r in _rules]):
                file_util.write_file(t, lambda f: f.write(file_util.read_file(t, lambda tf: template_util.Template(tf.read()).render(**role_env))))
        role_build_sh = role_path.joinpath("build.sh")
        if args.build_file == "build.sh":
            if role_build_sh.exists():
                run_cmd(collection_util.flat_to_str([
                    role_print(role_title, "build", role_build_sh.as_posix()),
                    "bash {0}".format(role_build_sh.as_posix())
                ], delimiter="&&"))
        role_func(role_title=role_title, role_path=role_path, role_env_dict=role_env, args=args, logger=logger, **kwargs)


class Installer:
    def __init__(self, root_path: pathlib.Path, role_func, role_deep: int = 1) -> None:
        log_util.init_logger()
        self.root_path: pathlib.Path = root_path
        self.bak_path: pathlib.Path = root_path.joinpath("___temp/bak")
        self.env_file: pathlib.Path = root_path.joinpath("env.yaml")
        self.jinja2ignore_file: pathlib.Path = root_path.joinpath(".jinja2ignore")
        self.role_func = role_func
        self.role_deep: int = role_deep
        self.arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()

    def run(self, **kwargs):
        self.arg_parser.add_argument('-p', '--param', nargs="+", default=[])
        self.arg_parser.add_argument('-i', '--install', action="store_true")
        self.arg_parser.add_argument('-d', '--delete', action="store_true")
        self.arg_parser.add_argument('-b', '--build-file', nargs='?', const="build.sh")
        self.arg_parser.add_argument('-a', '--action', type=str, required=False)
        self.arg_parser.add_argument('-n', '--namespace')
        self.arg_parser.add_argument('--debug', action="store_true")

        args: argparse.Namespace = self.arg_parser.parse_args()
        print("   args:", args)
        if args.debug:
            logger.setLevel(logging.DEBUG)
        # select role
        selected_role_dict, excludes = select_option(self.root_path, self.role_deep, args=args)
        global_env = {}
        # read env_file
        if self.env_file and self.env_file.exists():
            global_env.update(yaml_util.load(self.env_file))
        # read input param
        param_extra_iter = iter(args.param)
        param_extra_dict = dict(zip(param_extra_iter, param_extra_iter))
        global_env.update(param_extra_dict)
        # global env_dict finished
        global_jinja2ignore_rules = []
        if self.jinja2ignore_file and self.jinja2ignore_file.exists():
            global_jinja2ignore_rules = file_util.read_file(self.jinja2ignore_file, lambda f: [t.strip("\n") for t in f.readlines()])
        # loop selected_role_dict
        loop_role_dict(
            root_path=self.root_path,
            role_dict=selected_role_dict,
            role_func=self.role_func,
            global_env=global_env,
            jinja2ignore_rules=global_jinja2ignore_rules,
            args=args,
            bak_path=self.bak_path,
            **kwargs
        )
