import argparse
import logging
import os
import pathlib
import shutil
import sys
import typing
from abc import ABCMeta
from enum import Enum

import urllib3
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


class RoleMeta:
    def __init__(self, key: str, name: str, path: pathlib.Path, parent_path: pathlib.Path):
        self.key: str = key
        self.name: str = name
        self.path: pathlib.Path = path
        self.parent_path: pathlib.Path = parent_path


class Namespace:
    def __init__(self, name: str, roles: list[RoleMeta]):
        self.name = name
        self.roles = roles


class Command(Enum):
    install = "install"
    delete = "delete"
    backup = "backup"
    restore = "restore"
    build = "build"
    push = "push"


def dfs_dir(path: pathlib.Path, deep=1, exclude_rules: list = None, parent_key: str = "") -> list:
    ret = []
    _dirs = get_match_dirs(exclude_rules, filter(lambda a: a.is_dir(), sorted(path.iterdir())))
    for i, p in enumerate(_dirs, start=1):
        key = ".".join([parent_key, str(i)]) if parent_key != "" else str(i)
        ret.append({"path": p, "deep": deep, "key": key})
        ret += dfs_dir(p, deep + 1, exclude_rules, key)
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
        _rules = regex_util.match_rules(
            rules,
            p.as_posix(),
            ".jinja2ignore {0}".format(dfs_dir.__name__)
        )
        if not any(_rules.values()):
            _dirs.append(p)
    return _dirs


def echo_action(role, content, exec_file=None) -> str:
    c = "{} {} ".format(role, content)
    if exec_file:
        c += "=> {}".format(exec_file)
    return 'echo "' + c + '"'


def get_dir_dict(path: pathlib.Path, exclude_rules: list = None, select_tip="", col_num=5, args: argparse.Namespace = None) -> dict:
    _dirs = get_match_dirs(exclude_rules, list(filter(lambda a: a.is_dir(), sorted(path.iterdir()))))
    dir_dict: dict = {str(i): t for i, t in enumerate(_dirs, start=1)}
    collection_util.print_grid(["{0}.{1}".format(str(k), v.name) for k, v in dir_dict.items()], col_num=col_num, msg=path.as_posix())
    logger.info("\nplease select {0}:".format(select_tip))
    dir_nums = []
    if args.all_namespaces or args.all_roles:
        dir_nums.extend(dir_dict.keys())
    else:
        dir_nums.extend(input().strip().split())
    return dict((t, dir_dict[t]) for t in dir_nums if t in dir_dict.keys())


def select_namespace(root_path: pathlib.Path, deep: int = 1, exclude_rules=None, args: argparse.Namespace = None) -> list[Namespace]:
    exclude_rules = exclude_rules if exclude_rules else []
    exclude_rules.extend(["___temp", "build", root_path.joinpath("utility").as_posix(), root_path.joinpath("server").as_posix()])
    flat_dirs = dfs_dir(root_path, exclude_rules=exclude_rules)
    deep_index = 1
    namespaces = []
    if deep == deep_index:
        _root_path = pathlib.Path(root_path)
        namespaces.extend([
            Namespace(args.namespace if args.namespace else _root_path.name, [
                RoleMeta(rk, rv.name, rv, _root_path)
                for rk, rv in get_dir_dict(_root_path, exclude_rules=exclude_rules, select_tip="role num(example:1 2 ...)", args=args).items()
            ])
        ])
        return namespaces
    app_paths: list[pathlib.Path] = []
    while deep > deep_index:
        role_dict = {str(i): p for i, p in
                     enumerate(map(lambda a: a["path"], filter(lambda a: a["deep"] == deep_index, flat_dirs)), start=1)}
        collection_util.print_grid(["{0}.{1}".format(k, v.name) for k, v in role_dict.items()], col_num=5, msg=next(iter(role_dict.items()))[1].parent.as_posix())
        if args.all_namespaces:
            app_paths = list(role_dict.values())
        else:
            logger.info("\nplease select options(example:1 2 ...)")
            selected = input().strip()
            if selected == '':
                sys.exit()
            app_paths = [role_dict[t] for t in selected.split()]
        deep_index += 1
    namespaces.extend([
        Namespace(args.namespace if args.namespace else p.name,
                  [RoleMeta("%s.%s" % (next(filter(lambda t: t["path"] == p, flat_dirs), None)["key"], rk),
                            rv.name,
                            rv, p) for rk, rv in
                   get_dir_dict(p, exclude_rules=exclude_rules, select_tip="role num(example:1 2 ...)",
                                args=args).items()])
        for p in app_paths
    ])
    return namespaces


def execute(cmd, is_return: bool = False, dry_run=False):
    return basic_util.execute(cmd, is_input=False, is_return=is_return, stack_index=2, dry_run=dry_run)


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


class AbstractRole(metaclass=ABCMeta):

    def __init__(self,
                 home_path: pathlib.Path = None,
                 root_path: pathlib.Path = None,
                 namespace: str = None,
                 role_title: str = None,
                 role_name: str = None,
                 role_path: pathlib.Path = None,
                 role_output_path: pathlib.Path = None,
                 role_env: dict = None,
                 role_env_output_file: pathlib.Path = None,
                 args=None
                 ) -> None:
        self.home_path = home_path
        self.root_path = root_path
        self.role_title = role_title
        self.role_name = role_name
        self.role_path = role_path
        self.role_output_path = role_output_path
        self.role_env = role_env
        self.role_env_output_file = role_env_output_file
        self.namespace = namespace
        self.args = args

    def install(self) -> list[str]:
        pass

    def build(self) -> list[str]:
        pass

    def delete(self) -> list[str]:
        pass

    def backup(self) -> list[str]:
        pass

    def restore(self) -> list[str]:
        pass

    def push(self) -> list[str]:
        pass

    def sync_to_git_repo(self, role_platform_name):
        registry_git_repo_url: urllib3.util.Url = urllib3.util.parse_url(self.role_env.get("param_registry_git_repo"))
        registry_git_repo_name: str = pathlib.Path(registry_git_repo_url.path).name
        registry_git_repo_dir: pathlib.Path = self.home_path.joinpath(registry_git_repo_name)
        if not registry_git_repo_dir.exists():
            execute("git clone ssh://{0} {1}".format(registry_git_repo_url, registry_git_repo_dir))
        registry_git_repo_role_dir = registry_git_repo_dir.joinpath(self.role_name).joinpath(role_platform_name)
        registry_git_repo_role_dir.mkdir(exist_ok=True, parents=True)
        file_util.sync(self.role_output_path, self.any_doc_exclude, registry_git_repo_role_dir)

    def any_doc_exclude(self, f: pathlib.Path):
        return not any(regex_util.match_rules(self.role_env["param_doc_excludes"], f.as_posix()).values())


class Installer:
    def __init__(self, root_path: pathlib.Path, role_class: typing.Type[AbstractRole] = None, role_deep: int = 1) -> None:
        self.home_path: pathlib.Path = root_path.joinpath("..").resolve()
        self.root_path: pathlib.Path = root_path
        self.build_path: pathlib.Path = root_path.joinpath("build")
        self.tmp_path: pathlib.Path = root_path.joinpath("___temp")
        self.bak_path: pathlib.Path = self.tmp_path.joinpath("bak")
        self.env_file: pathlib.Path = root_path.joinpath("server/env.yaml")
        self.jinja2ignore_file: pathlib.Path = root_path.joinpath(".jinja2ignore")
        self.role_class: typing.Type[AbstractRole] = role_class
        self.role_deep: int = role_deep
        self.arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter, usage='%(prog)s [command] [options]')
        self.set_common_argument(self.arg_parser)
        self.__command_parser = self.arg_parser.add_subparsers(title="commands", metavar="", dest="command")
        self.__init_install_parser()
        self.__init_delete_parser()
        self.__init_build_parser()
        self.__init_backup_parser()
        self.__init_restore_parser()
        self.__init_push_parser()

        log_util.init_logger(file=self.build_path.joinpath("share.log"))
        self.tmp_path.mkdir(exist_ok=True)
        self.build_path.mkdir(exist_ok=True)

    @staticmethod
    def load_env_file(env_file: pathlib.Path, env_file_names: list[str]):
        d = {}
        env_self_file = env_file.parent.parent.joinpath(env_file.name)
        env_file_paths: list[pathlib.Path] = [env_file, env_self_file]

        def add_env_file(f):
            for ef in env_file_names:
                ef = f.parent.joinpath(ef)
                if not ef.is_absolute():
                    ef = pathlib.Path.cwd().joinpath(ef)
                if ef not in env_file_paths:
                    env_file_paths.append(ef)

        add_env_file(env_file)
        add_env_file(env_self_file)
        env_file_paths = sorted(set(env_file_paths), key=env_file_paths.index)
        for t in env_file_paths:
            if t.exists():
                logger.info("load env_file: %s" % t.as_posix())
                d |= yaml_util.load(t)
        return d

    @staticmethod
    def set_common_argument(parser: argparse.ArgumentParser):
        parser.add_argument('-n', '--namespace', type=str)
        parser.add_argument('-p', '--param', nargs="+", default=[], type=lambda s: dict({split_kv_str(s)}), help="k1=v1 k2=v2")
        parser.add_argument('--env-file', nargs="+", default=[], help="file1.yaml file2.yaml")
        parser.add_argument('--all-roles', action="store_true")
        parser.add_argument('--all-namespaces', action="store_true")
        parser.add_argument('--ignore-namespace', action="store_true")
        parser.add_argument('--create-namespace', action="store_true")
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
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.install.value))
        self.set_common_argument(parser)
        parser.add_argument('--rm-conf', action="store_true", help="rm target conf")
        parser.add_argument('--recreate', action="store_true")

    def __init_delete_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.delete.value))
        self.set_common_argument(parser)

    def __init_build_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.build.value))
        self.set_common_argument(parser)
        parser.add_argument("--target", type=str, default="build.sh", help="(default=build.sh)")
        parser.add_argument('--build-args', nargs="+", default=[])
        parser.add_argument('--tag')
        parser.add_argument('--push', action="store_true")

    def __init_backup_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.backup.value))
        self.set_common_argument(parser)

    def __init_restore_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.restore.value))
        self.set_common_argument(parser)

    def __init_push_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.push.value))
        self.set_common_argument(parser)

    def __loop_namespaces(self, namespaces: list[Namespace], global_env: dict, args: argparse.Namespace, jinja2ignore_rules: list) -> None:
        for n in namespaces:
            namespace = n.name
            for r in n.roles:
                role_key = r.key
                role_name = r.name
                role_path: pathlib.Path = r.path
                role_title = "%s.%s" % (role_key, role_name)
                role_temp_path = role_path.joinpath("___temp")
                role_temp_path.mkdir(parents=True, exist_ok=True)
                role_bak_path = role_temp_path.joinpath("bak")
                role_build_path = role_path.joinpath("build")
                role_build_path.mkdir(parents=True, exist_ok=True)
                role_output_path = role_build_path.joinpath("output")
                shutil.rmtree(role_output_path, ignore_errors=True)
                role_env_file = role_path.joinpath("env.yaml")
                role_env_output_file = role_output_path.joinpath("env.yaml")
                role_env = {} | global_env | {
                    "param_role_name": role_name,
                    "param_role_path": role_path.as_posix(),
                    "param_role_title": role_title,
                    "param_role_build_path": role_build_path.as_posix(),
                    "param_role_output_path": role_output_path.as_posix(),
                    "param_role_temp_path": role_temp_path.as_posix(),
                    "param_role_bak_path": role_bak_path.as_posix()
                }
                if args.command == Command.backup.value:
                    role_bak_path.mkdir(exist_ok=True)
                # process env
                if role_env_file and role_env_file.exists():
                    role_env |= yaml_util.load(template_util.Template(file_util.read_text(role_env_file)).render(**role_env))
                file_util.write_text(role_env_output_file, yaml.dump(role_env))
                role_env |= args.param
                # process template
                for t in filter(lambda f: f.is_file() and not any(regex_util.match_rules(["build/"], f.as_posix()).values()), role_path.rglob("*")):
                    _rules = regex_util.match_rules(
                        [*jinja2ignore_rules, "___temp/"],
                        t.as_posix(),
                        ".jinja2ignore {0}".format(self.__loop_namespaces.__name__)
                    )
                    role_output_file = role_output_path.joinpath(t.relative_to(role_path))
                    if not any(_rules.values()):
                        file_util.write_text(role_output_file, template_util.Template(file_util.read_text(t)).render(**role_env))
                    else:
                        file_util.copy(t, role_output_file)

                # collect command
                _cmds = [
                    echo_action(role_title, args.command)
                ]
                if args.command == Command.build.value:
                    if args.target == "build.sh":
                        target_file = role_output_path.joinpath(args.target)
                        if target_file.exists():
                            _cmds.append(echo_action(role_title, Command.build.value, target_file.as_posix()))
                            _cmds.append("sh {0} {1}".format(target_file.as_posix(), " ".join(args.build_args)))
                role_instance = self.role_class(home_path=self.home_path,
                                                root_path=self.root_path,
                                                role_title=role_title,
                                                role_name=role_name,
                                                role_path=role_path,
                                                role_output_path=role_output_path,
                                                role_env=role_env,
                                                role_env_output_file=role_env_output_file,
                                                namespace=namespace,
                                                args=args)
                _cmds.extend(getattr(role_instance, args.command)())
                execute(collection_util.flat_to_str(_cmds, delimiter=" && "), dry_run=args.dry_run)

                def cp_role_to_root(src: pathlib.Path, dst: pathlib.Path):
                    return "mkdir -p {0} && cp -r {1} {0}".format(dst.joinpath(role_path.relative_to(self.root_path)).as_posix(), src.as_posix())

                execute(collection_util.flat_to_str([
                    cp_role_to_root(role_build_path, self.build_path),
                    cp_role_to_root(role_temp_path, self.tmp_path)
                ], delimiter=" && "))

    def run(self, **kwargs):
        args: argparse.Namespace = self.arg_parser.parse_args()
        args.param = {k: v for t in args.param for (k, v) in t.items()}
        logger.info("args: {0}".format(args))
        if args.debug:
            logger.setLevel(logging.DEBUG)
        global_env = self.load_env_file(self.env_file, args.env_file)
        global_env["param_command"] = args.command
        global_jinja2ignore_rules = file_util.read_text(self.jinja2ignore_file).split("\n") if self.jinja2ignore_file and self.jinja2ignore_file.exists() else []
        namespaces = select_namespace(self.root_path, self.role_deep, args=args)
        for n in namespaces:
            logger.info("namespace: {0}; roles: {1}".format(n.name, ",".join(["%s.%s" % (r.key, r.name) for r in n.roles])))
        self.__loop_namespaces(
            namespaces=namespaces,
            global_env=global_env,
            jinja2ignore_rules=global_jinja2ignore_rules,
            args=args
        )


if __name__ == '__main__':
    log_util.init_logger(file=pathlib.Path(__file__).parent.joinpath("___temp/share.log"))
    logger.setLevel(logging.DEBUG)
    select_namespace(pathlib.Path(__file__).parent.joinpath("docker"), deep=2)
    # Installer(pathlib.Path(__file__).parent).run()
