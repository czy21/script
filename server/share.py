import argparse
import json
import logging
import os
import pathlib
import sys
import typing

import yaml

from utility import (
    collection as collection_util,
    file as file_util,
    regex as regex_util,
    template as template_util,
    yaml as yaml_util,
    log as log_util,
    basic as basic_util
)

logger = logging.getLogger()


def dfs_dir(path: pathlib.Path, deep=1, exclude_rules: list = None) -> list:
    ret = []
    _dirs = get_match_dirs(exclude_rules, list(filter(lambda a: a.is_dir(), sorted(path.iterdir()))))
    for p in _dirs:
        ret.append({"path": p, "deep": deep})
        ret += dfs_dir(p, deep + 1, exclude_rules)
    return ret


def split_kv_str(kv_str) -> (str, str):
    for i in range(len(kv_str)):
        if kv_str[i] == "=":
            k = ''.join(kv_str[0:i])
            v = ''.join(kv_str[i + 1:])
            return k, v


def get_match_dirs(rules, items):
    _dirs = []
    for p in items:
        _rules = regex_util.match_rules(rules, p.as_posix(), ".jinia2ignore {0}".format(dfs_dir.__name__))
        if not any([r["isMatch"] for r in _rules]):
            _dirs.append(p)
    return _dirs


def echo_action(role, content, exec_file=None) -> str:
    c = "{} {} ".format(role, content)
    if exec_file:
        c += "=> {}".format(exec_file)
    return 'echo "' + c + '"'


def get_dir_dict(root_path: pathlib.Path, exclude_rules: list = None, select_tip="", col_num=5) -> dict:
    _dirs = get_match_dirs(exclude_rules, list(filter(lambda a: a.is_dir(), sorted(root_path.iterdir()))))
    dir_dict: dict = {str(i): t for i, t in enumerate(_dirs, start=1)}
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


def execute(cmd, is_return: bool = False, dry_run=False):
    return basic_util.execute(cmd, is_input=False, is_return=is_return, stack_index=2, dry_run=dry_run)


def loop_roles(root_path: pathlib.Path,
               tmp_path: pathlib.Path,
               bak_path: pathlib.Path,
               roles: dict,
               role_func: typing.Callable[..., None],
               global_env: dict,
               args: argparse.Namespace,
               jinja2ignore_rules: list,
               **kwargs) -> None:
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

        def build_target(file_name: str):
            build_file = role_path.joinpath(file_name)
            if args.file == file_name:
                if build_file.exists():
                    execute(collection_util.flat_to_str([
                        echo_action(role_title, file_name, build_file.as_posix()),
                        "sh {0} {1}".format(build_file.as_posix(), " ".join(args.build_args))
                    ], delimiter="&&"))

        build_target("build.sh")
        if role_func:
            role_func(role_title=role_title, role_path=role_path, role_env=role_env, args=args, **kwargs)
        execute("mkdir -p {1} && cp -r {0}/* {1}".format(role_path, tmp_path.joinpath(args.namespace).joinpath(role_name)))


class CustomHelpFormatter(argparse.MetavarTypeHelpFormatter):
    def add_arguments(self, actions: typing.Iterable[argparse.Action]) -> None:
        for a in sorted(actions, key=lambda i: i.dest[0:1]):
            self.add_argument(a)

    def _format_args(self, action: argparse.Action, default_metavar: str) -> str:
        result = default_metavar
        if action.nargs == argparse.ONE_OR_MORE:
            result = list.__name__
        return result

    def _format_actions_usage(self, actions, groups) -> str:
        return ''

    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                args_prefix = next(filter(lambda a: a.startswith("--"), action.option_strings), None)
                for option_string in action.option_strings:
                    if option_string == args_prefix:
                        parts.append('%s %s' % (args_prefix, args_string))
                    else:
                        parts.append(option_string)
        return ', '.join(t.strip() for t in parts)

    def _get_default_metavar_for_optional(self, action: argparse.Action) -> str:
        if action.type:
            return action.type.__name__

    def _get_default_metavar_for_positional(self, action: argparse.Action) -> str:
        if action.type:
            return action.type.__name__


class Installer:
    def __init__(self,
                 root_path: pathlib.Path,
                 role_func: typing.Callable[..., None] = None,
                 role_deep: int = 1
                 ) -> None:
        self.root_path: pathlib.Path = root_path
        self.tmp_path: pathlib.Path = root_path.joinpath("___temp")
        self.bak_path: pathlib.Path = self.tmp_path.joinpath("bak")
        self.env_file: pathlib.Path = root_path.joinpath("env.yaml")
        self.jinja2ignore_file: pathlib.Path = root_path.joinpath(".jinja2ignore")
        self.role_func: typing.Callable[..., None] = role_func
        self.role_deep: int = role_deep
        self.arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter, usage='%(prog)s [command] [options]')
        self.set_common_argument(self.arg_parser)
        self.__command_parser = self.arg_parser.add_subparsers(title="commands", metavar="", dest="command")
        self.__init_install_parser()
        self.__init_delete_parser()
        self.__init_build_parser()
        self.__init_backup_parser()
        self.__init_push_parser()

        log_util.init_logger(file=root_path.joinpath("___temp/share.log"))
        self.tmp_path.mkdir(exist_ok=True)

    @staticmethod
    def set_common_argument(parser: argparse.ArgumentParser):
        parser.add_argument('--file', type=str)
        parser.add_argument('-n', '--namespace', type=str)
        parser.add_argument('-p', '--param', nargs="+", default=[], type=lambda s: dict({split_kv_str(s)}), help="k1=v1 k2=v2")
        parser.add_argument('--debug', action="store_true", help="enable verbose output")
        parser.add_argument('--dry-run', action="store_true", help="only print not submit")

    @staticmethod
    def __get_sub_parser_common_attr(name):
        return {
            "prog": "{0} {1}".format(os.path.basename(sys.argv[0]), name),
            "name": name,
            "usage": "%(prog)s [options]",
            "formatter_class": CustomHelpFormatter,
            "help": "",
        }

    def __init_install_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr("install"))
        self.set_common_argument(parser)
        parser.add_argument('--recreate', action="store_true")

    def __init_delete_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr("delete"))
        self.set_common_argument(parser)

    def __init_build_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr("build"))
        self.set_common_argument(parser)
        parser.add_argument('--build-args', nargs="+", default=[])
        parser.add_argument('--tag')

    def __init_backup_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr("backup"))
        self.set_common_argument(parser)

    def __init_push_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr("push"))
        self.set_common_argument(parser)

    def run(self, **kwargs):
        args: argparse.Namespace = self.arg_parser.parse_args()
        args.param = {k: v for t in args.param for (k, v) in t.items()}
        logger.info("args: {0}".format(args))
        if args.debug:
            logger.setLevel(logging.DEBUG)
        selected_roles = select_role(self.root_path, self.role_deep, args=args)
        logger.info("namespace: {0}; selected roles: {1}".format(args.namespace, ",".join(["{0}.{1}".format(k, v.name) for k, v in selected_roles.items()])))
        global_env = yaml_util.load(self.env_file) if self.env_file and self.env_file.exists() else {}
        global_env.update(args.param)
        global_jinja2ignore_rules = file_util.read_text(self.jinja2ignore_file).split("\n") if self.jinja2ignore_file and self.jinja2ignore_file.exists() else []
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


if __name__ == '__main__':
    Installer(pathlib.Path(__file__).parent).run()
