import argparse
import json
import logging
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
    return basic_util.execute(cmd, is_input=False, is_return=is_return, dry_run=dry_run)


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


class CustomHelpFormatter(argparse.HelpFormatter):
    def add_arguments(self, actions: typing.Iterable[argparse.Action]) -> None:
        super().add_arguments(sorted(actions, key=lambda a: a.dest))

    def _format_args(self, action: argparse.Action, default_metavar: str) -> str:
        # get_metavar = self._metavar_formatter(action, default_metavar)
        # if action.nargs is None:
        #     result = '%s' % get_metavar(1)
        # elif action.nargs == argparse.OPTIONAL:
        #     result = '[%s]' % get_metavar(1)
        # elif action.nargs == argparse.ZERO_OR_MORE:
        #     metavar = get_metavar(1)
        #     if len(metavar) == 2:
        #         result = '[%s [%s ...]]' % metavar
        #     else:
        #         result = '[%s ...]' % metavar
        # elif action.nargs == argparse.ONE_OR_MORE:
        #     result = '%s [%s ...]' % get_metavar(2)
        # elif action.nargs == argparse.REMAINDER:
        #     result = '...'
        # elif action.nargs == argparse.PARSER:
        #     result = '%s ...' % get_metavar(1)
        # elif action.nargs == argparse.SUPPRESS:
        #     result = ''
        # else:
        #     try:
        #         formats = ['%s' for _ in range(action.nargs)]
        #     except TypeError:
        #         raise ValueError("invalid nargs value") from None
        #     result = ' '.join(formats) % get_metavar(action.nargs)
        return ''

    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts = []

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s %s' % (option_string, args_string))
        return ', '.join(t.strip() for t in parts)


class Installer:
    def __init__(self, root_path: pathlib.Path, role_func=None, role_deep: int = 1) -> None:
        self.root_path: pathlib.Path = root_path
        self.tmp_path: pathlib.Path = root_path.joinpath("___temp")
        self.bak_path: pathlib.Path = self.tmp_path.joinpath("bak")
        self.env_file: pathlib.Path = root_path.joinpath("env.yaml")
        self.jinja2ignore_file: pathlib.Path = root_path.joinpath(".jinja2ignore")
        self.role_func = role_func
        self.role_deep: int = role_deep
        self.usage_name = pathlib.Path(__file__).name
        self.arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
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
        parser.add_argument('--file')
        parser.add_argument('-n', '--namespace')
        parser.add_argument('-p', '--param', nargs="+", default=[], metavar=('', 'key1=val1 key2=val2'))
        parser.add_argument('--debug', action="store_true", help=" enable verbose output")
        parser.add_argument('--dry-run', action="store_true", help="only print not submit")

    @staticmethod
    def __get_sub_parser_common_attr():
        return {
            "help": "",
            "formatter_class": CustomHelpFormatter
        }

    def __init_install_parser(self):
        install_parser = self.__command_parser.add_parser("install", **self.__get_sub_parser_common_attr())
        self.set_common_argument(install_parser)
        install_parser.add_argument('--recreate', action="store_true")

    def __init_delete_parser(self):
        delete_parser = self.__command_parser.add_parser("delete", **self.__get_sub_parser_common_attr())
        self.set_common_argument(delete_parser)

    def __init_build_parser(self):
        build_parser = self.__command_parser.add_parser("build", **self.__get_sub_parser_common_attr())
        self.set_common_argument(build_parser)
        build_parser.add_argument('--build-args', nargs="+", default=[])
        build_parser.add_argument('--tag')

    def __init_backup_parser(self):
        backup_parser = self.__command_parser.add_parser("backup", **self.__get_sub_parser_common_attr())
        self.set_common_argument(backup_parser)

    def __init_push_parser(self):
        push_parser = self.__command_parser.add_parser("push", **self.__get_sub_parser_common_attr())
        self.set_common_argument(push_parser)

    def run(self, **kwargs):
        args: argparse.Namespace = self.arg_parser.parse_args()
        logger.info("args: {0}".format(args))
        if args.debug:
            logger.setLevel(logging.DEBUG)
        # select role
        selected_roles = select_role(self.root_path, self.role_deep, args=args)
        logger.info("namespace: {0}; selected roles: {1}".format(args.namespace, ",".join(["{0}.{1}".format(k, v.name) for k, v in selected_roles.items()])))
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


if __name__ == '__main__':
    Installer(pathlib.Path(__file__).parent).run()
