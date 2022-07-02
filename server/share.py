import argparse
import json
import logging
import pathlib
import subprocess
import sys

import yaml

from utility import collection as collection_util, file as file_util, regex as regex_util, template as template_util, yaml as yaml_util, log as log_util

logger = logging.getLogger()


def dfs_dir(path: pathlib.Path, deep=1, exclude_rules: list = None) -> list:
    ret = []
    _include_dirs = []
    for p in list(filter(lambda a: a.is_dir(), sorted(path.iterdir()))):
        _rules = regex_util.match_rules(exclude_rules, p.as_posix(), ".jinia2ignore {0}".format(dfs_dir.__name__))
        if not any([r["isMatch"] for r in _rules]):
            _include_dirs.append(p)
    for p in _include_dirs:
        ret.append({"path": p, "deep": deep})
        ret += dfs_dir(p, deep + 1, exclude_rules)
    return ret


def echo_action(role, content, exec_file=None) -> str:
    c = "{} {} ".format(role, content)
    if exec_file:
        c += "=> {}".format(exec_file)
    return 'echo "' + c + '"'


def get_dir_dict(root_path: pathlib.Path, exclude_rules: list = None, select_tip="", col_num=5) -> dict:
    _include_dirs = []
    for p in list(filter(lambda a: a.is_dir(), sorted(root_path.iterdir()))):
        _rules = regex_util.match_rules(exclude_rules, p.as_posix(), ".jinia2ignore {0}".format(get_dir_dict.__name__))
        if not any([r["isMatch"] for r in _rules]):
            _include_dirs.append(p)
    dir_dict: dict = {str(i): t for i, t in enumerate(_include_dirs, start=1)}
    collection_util.print_grid(["{0}.{1}".format(str(k), v.name) for k, v in dir_dict.items()], col_num=col_num)
    logger.info("\nplease select {0}:".format(select_tip))
    dir_nums = input().strip().split()
    return dict((t, dir_dict[t]) for t in dir_nums if t in dir_dict.keys())


def select_role(root_path: pathlib.Path, deep: int = 1, exclude_rules=None, args: argparse.Namespace = None):
    exclude_rules = exclude_rules if exclude_rules else []
    exclude_rules.extend(["___temp", "utility"])
    flat_dirs = dfs_dir(root_path, exclude_rules=exclude_rules)

    app_path = root_path
    deep_index = 1

    while deep > deep_index:
        role_dict = {str(i): p for i, p in enumerate(map(lambda a: a["path"], filter(lambda a: a["deep"] == deep_index, flat_dirs)), start=1)}
        collection_util.print_grid(["{0}.{1}".format(k, v.name) for k, v in role_dict.items()], col_num=5)
        logger.info("\nplease select one option(example:1)")
        selected = input().strip()
        logger.info("namespace: {0}".format(selected))
        if selected == '':
            sys.exit()
        if selected not in role_dict.keys():
            logger.error("{0} not exist".format(selected))
            sys.exit()
        app_path = role_dict[selected]
        deep_index = deep_index + 1
    if args.namespace is None:
        args.namespace = app_path.name
    return get_dir_dict(app_path, exclude_rules=exclude_rules, select_tip="role num(example:1 2 3)")


def run_cmd(cmd):
    logger.debug(cmd)
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8") as proc:
        logger.info(proc.stdout.read())
        proc.stdout.close()
        proc.wait()
        if proc.returncode != 0:
            sys.exit(0)


def loop_roles(root_path: pathlib.Path,
               tmp_path: pathlib.Path,
               bak_path: pathlib.Path,
               roles: dict,
               role_func,
               global_env,
               args: argparse.Namespace,
               jinja2ignore_rules: list,
               **kwargs):
    for k, v in roles.items():
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
            role_env.update(yaml_util.load(template_util.Template(file_util.read_text(role_env_file)).render(**role_env)))
            file_util.write_text(role_env_file, yaml.dump(role_env))
        logger.debug("{0} params: {1}".format(role_name, json.dumps(role_env, indent=1)))
        # write jinja2 template
        for t in filter(lambda f: f.is_file(), role_path.rglob("*")):
            _rules = regex_util.match_rules([*jinja2ignore_rules, pathlib.Path(role_name).joinpath("env.yaml").as_posix()], t.as_posix(), ".jinia2ignore {0}".format(loop_roles.__name__))
            if not any([r["isMatch"] for r in _rules]):
                file_util.write_text(t, template_util.Template(file_util.read_text(t)).render(**role_env))
        role_build_sh = role_path.joinpath("build.sh")
        if args.build_file == "build.sh":
            if role_build_sh.exists():
                run_cmd(collection_util.flat_to_str([
                    echo_action(role_title, "build", role_build_sh.as_posix()),
                    "bash {0}".format(role_build_sh.as_posix())
                ], delimiter="&&"))
        role_func(role_title=role_title, role_path=role_path, role_env=role_env, args=args, **kwargs)
        run_cmd("mkdir -p {1} && cp -r {0}/* {1}".format(role_path, tmp_path.joinpath(args.namespace).joinpath(role_name)))


class Installer:
    def __init__(self, root_path: pathlib.Path, role_func, role_deep: int = 1) -> None:
        self.root_path: pathlib.Path = root_path
        self.tmp_path: pathlib.Path = root_path.joinpath("___temp")
        self.bak_path: pathlib.Path = self.tmp_path.joinpath("bak")
        self.env_file: pathlib.Path = root_path.joinpath("env.yaml")
        self.jinja2ignore_file: pathlib.Path = root_path.joinpath(".jinja2ignore")
        self.role_func = role_func
        self.role_deep: int = role_deep
        self.arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()

        log_util.init_logger(file=root_path.joinpath("___temp/share.log"))

    def run(self, **kwargs):
        self.arg_parser.add_argument('-p', '--param', nargs="+", default=[])
        self.arg_parser.add_argument('-i', '--install', action="store_true")
        self.arg_parser.add_argument('-d', '--delete', action="store_true")
        self.arg_parser.add_argument('-b', '--build-file', nargs='?', const="build.sh")
        self.arg_parser.add_argument('-a', '--action', type=str, required=False)
        self.arg_parser.add_argument('-n', '--namespace')
        self.arg_parser.add_argument('--debug', action="store_true")

        args: argparse.Namespace = self.arg_parser.parse_args()
        logger.info("args: {0}".format(args))
        if args.debug:
            logger.setLevel(logging.DEBUG)
        # select role
        selected_roles = select_role(self.root_path, self.role_deep, args=args)
        logger.info("namespace: {0}; selected roles: {1}".format(args.namespace, ",".join(selected_roles.keys())))
        global_env = yaml_util.load(self.env_file) if self.env_file and self.env_file.exists() else {}
        # read input param
        param_extra_iter = iter(args.param)
        global_env.update(dict(zip(param_extra_iter, param_extra_iter)))
        # global env_dict finished
        global_jinja2ignore_rules = file_util.read_text(self.jinja2ignore_file).split("\n") if self.jinja2ignore_file and self.jinja2ignore_file.exists() else []
        # loop selected_role_dict
        loop_roles(
            root_path=self.root_path,
            tmp_path=self.tmp_path,
            bak_path=self.bak_path,
            roles=selected_roles,
            role_func=self.role_func,
            global_env=global_env,
            jinja2ignore_rules=global_jinja2ignore_rules,
            args=args,
            **kwargs
        )
