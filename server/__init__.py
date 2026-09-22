import json
import logging
import os
import re
import shutil
import sys
import typing
from abc import ABCMeta
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

import argparse
import pathlib
import requests

from util import (
    collection as collection_util,
    file as file_util,
    regex as regex_util,
    template as template_util,
    yaml as yaml_util,
    log as log_util,
    basic as basic_util,
    path as path_util
)

logger = logging.getLogger()


class RoleMeta(typing.NamedTuple):
    root_path: pathlib.Path
    role_path: pathlib.Path
    role_name: str
    namespace: str


class Command(Enum):
    install = "install"
    restore = "restore"
    delete = "delete"
    backup = "backup"
    build = "build"


def dfs_dir(path: pathlib.Path, deep=1, exclude_rules: list | None = None, parent_key: str = "") -> list:
    ret = []
    _dirs = get_match_dirs(exclude_rules, filter(lambda a: a.is_dir(), sorted(path.iterdir())))
    for i, p in enumerate(_dirs, start=1):
        key = ".".join([parent_key, str(i)]) if parent_key != "" else str(i)
        ret.append({"path": p, "deep": deep, "key": key})
        ret += dfs_dir(p, deep + 1, exclude_rules, key)
    return ret


def get_match_dirs(rules, items):
    _dirs = []
    for p in items:
        _rules = regex_util.match_rules(rules, p.as_posix() + "/", ".jinja2ignore {0}".format(dfs_dir.__name__))
        if not any(_rules.values()):
            _dirs.append(p)
    return _dirs


def echo_action(role, content, exec_file=None) -> str:
    c = "{} {}".format(role, content)
    if exec_file:
        c += " => {}".format(exec_file)
    return 'echo "' + c + '"'


def get_dir_dict(path: pathlib.Path, exclude_rules: list | None = None, select_tip="", col_num=5, args: argparse.Namespace | None = None) -> dict:
    _dirs = get_match_dirs(exclude_rules, list(filter(lambda a: a.is_dir(), sorted(path.iterdir()))))
    dir_dict: dict = {str(i): t for i, t in enumerate(_dirs, start=1)}
    if 'all' not in args.roles and select_tip:
        collection_util.print_grid(["{0}.{1}".format(str(k), v.name) for k, v in dir_dict.items()], col_num=col_num, msg=path.as_posix())
        logger.info("\nplease select {0}:".format(select_tip))
    dir_nums = dir_dict.keys() if args.roles else input().strip().split()
    return dict((t, dir_dict[t]) for t in dir_nums if t in dir_dict.keys())


def select_roles(root_path: pathlib.Path, deep: int, args: argparse.Namespace, exclude_rules=None) -> list[RoleMeta]:
    col_num = 5
    exclude_rules = exclude_rules or []
    exclude_rules.extend(["build/", ".tmp/", root_path.joinpath("util").as_posix(), root_path.joinpath("server").as_posix()])
    flat_dirs = dfs_dir(root_path, exclude_rules=exclude_rules)
    deep_index = 1
    roles = []
    
    if not args.roles or 'all' in args.roles:
        if deep == deep_index:
            roles.extend([
                RoleMeta(root_path=root_path, role_path=rv, role_name=rv.name, namespace=args.namespace or root_path.name)
                for rk, rv in get_dir_dict(root_path, exclude_rules=exclude_rules, select_tip="role num(example:1 2 ...)", args=args).items()
            ])
            return roles
        app_paths: list[pathlib.Path] = []
        while deep > deep_index:
            role_dict = {
                str(i): p
                for i, p in enumerate(map(lambda a: a["path"], filter(lambda a: a["deep"] == deep_index, flat_dirs)), start=1)
            }
            if 'all' in args.roles:
                app_paths = list(role_dict.values())
            else:
                collection_util.print_grid(["{0}.{1}".format(k, v.name) for k, v in role_dict.items()], col_num=col_num, msg=next(iter(role_dict.items()))[1].parent.as_posix())
                logger.info("\nplease select options(example:1 2 ...)")
                selected = input().strip()
                if selected == '':
                    sys.exit()
                app_paths = [role_dict[t] for t in selected.split()]
            deep_index += 1
        for p in app_paths:
            roles.extend([
                RoleMeta(root_path=root_path, role_path=rv, role_name=rv.name, namespace=args.namespace or p.name)
                for rk, rv in get_dir_dict(p, exclude_rules=exclude_rules, select_tip="role num(example:1 2 ...)", col_num=col_num, args=args).items()
            ])
    else:
        for r in args.roles:
            role_path = root_path.joinpath(r)
            if not role_path.exists(): continue
            roles.extend([
                RoleMeta(root_path=root_path, role_path=rv, role_name=rv.name, namespace=args.namespace or (root_path.name if deep == deep_index else role_path.parent.name))
                for rk, rv in get_dir_dict(role_path.parent, exclude_rules=exclude_rules, select_tip="", args=args).items()
                if rv == role_path
            ])
    return roles


def execute(cmd, is_return: bool = False, dry_run=False):
    return basic_util.execute(cmd, is_input=False, is_return=is_return, dry_run=dry_run)


class ArgParseHelpFormatter(argparse.MetavarTypeHelpFormatter):
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
        return action.type.__name__ if action.type and action.type.__name__ else str.__name__

    def _get_default_metavar_for_positional(self, action: argparse.Action) -> str:
        return action.type.__name__ if action.type and action.type.__name__ else str.__name__


class RoleContext(typing.NamedTuple):
    root_path: pathlib.Path
    role_path: pathlib.Path
    role_name: str
    namespace: str

    args: argparse.Namespace
    role_env: dict[str, typing.Any]
    role_node_path: pathlib.Path

    role_build_path: pathlib.Path
    role_doc_path: pathlib.Path
    role_out_path: pathlib.Path


class AbstractRole(metaclass=ABCMeta):

    def __init__(self, context: RoleContext) -> None:
        self.context = context
        self.root_doc_template_file = context.root_path.joinpath("doc-template.md")
        self.role_doc_content: str = ""

    def install(self) -> list[str]:
        pass

    def build(self) -> list[str]:
        pass

    def get_check_images(self, images_file):
        token_cache = {}
        images = []
        if not images_file.exists():
            return images
        
        mirror_host = self.context.role_env.get('param_mirror_host')

        def get_repository_cache(token_url, namespace, name):
            url = f"{token_url}/token?service=registry.docker.io&scope=repository:{namespace}/{name}:pull"
            token = token_cache.get(url)
            if not token:
                token = requests.get(url).json().get("token")
                token_cache[url] = token
            return token

        for l in file_util.read_text(images_file).splitlines():
            l = l.split("@", 1)[0].rstrip(":")
            parts = l.split("/")
            registry = parts.pop(0) if len(parts) > 1 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost") else "docker.io"
            if not parts: continue
            namespace = "/".join(parts[:-1]) or "library"
            name, sep, version = parts[-1].rpartition(":")
            if not sep:
                name = parts[-1]
                version = "latest"
            if version == "latest": continue
            version_major_match = re.match(r'v?(\d+)', version)
            version_major = int(version_major_match.group(1)) if version_major_match else None

            if registry == "docker.io":
                api_url = "https://registry-1.docker.io"
                web_url = "https://hub.docker.com/r"
                token_url = "https://auth.docker.io"
                proxy_url = f"https://{mirror_host}/docker-proxy"

            elif registry == "mcr.microsoft.com":
                api_url = f"https://{registry}"
                web_url = api_url
                token_url = None
                proxy_url = f"https://{mirror_host}/docker-proxy-mcr"
            else:
                api_url = f"https://{registry}"
                web_url = api_url
                token_url = f"https://{registry}"
                proxy_url = f"https://{mirror_host}/docker-proxy-{registry.replace('.io', '')}"

            try:
                image = {'name': f'{registry}/{namespace}/{name}', 'version': version, 'repository': f"{web_url}/{namespace}/{name}"}
                if self.context.args.check:
                    if registry not in self.context.role_env.get('param_registry_checks', []):
                        logger.debug(f"{image.get('name')}: ignore check")
                        continue
                    repository_token = get_repository_cache(token_url, namespace, name) if token_url and not self.context.args.proxy else None
                    repository_headers = {}
                    if repository_token:
                        repository_headers["Authorization"] = f"Bearer {repository_token}"
                    image_tags = requests.get(f"{proxy_url if self.context.args.proxy else api_url}/v2/{namespace}/{name}/tags/list?n=10000", headers=repository_headers).json()
                    image_tags = sorted((x for x in image_tags.get("tags", []) if basic_util.get_version_number(x)), key=basic_util.get_version_number, reverse=True)
                    image['latest'] = max((x for x in image_tags if (v := basic_util.get_version_number(x)) and v[0] == version_major), key=basic_util.get_version_number, default=None) or version
                images.append(image)
            except Exception as e:
                logger.error(f"{self.context.role_path}: {e}")
        return images

    def delete(self) -> list[str]:
        pass

    def backup(self) -> list[str]:
        pass

    def restore(self) -> list[str]:
        pass

    def get_merge_ignore_pattern(self):
        return []


class Installer:
    def __init__(self, root_path: pathlib.Path,
                 arg_parser: argparse.ArgumentParser | None = None,
                 role_impl: typing.Type[AbstractRole] | None = None,
                 role_deep: int = 1) -> None:
        self.root_path: pathlib.Path = root_path

        self.role_impl: typing.Type[AbstractRole] | None = role_impl
        self.role_deep: int = role_deep
        self.arg_parser: argparse.ArgumentParser = arg_parser or argparse.ArgumentParser(formatter_class=ArgParseHelpFormatter, usage='%(prog)s [command] [options]')
        self.set_common_argument(self.arg_parser)

        self.tmp_path: pathlib.Path = root_path.joinpath(".tmp")
        self.bak_path: pathlib.Path = self.tmp_path.joinpath("bak")
        self.jinja2ignore_file: pathlib.Path = root_path.joinpath(".jinja2ignore")

        log_util.init_logger(file=self.root_path.joinpath("build.log"))
        [t.mkdir(exist_ok=True) for t in [self.tmp_path]]

    def load_env_file(self, env_active: list[str] | None = None, env_extra: dict | None = None) -> dict:
        env_files = []

        def scan_env_files(src_env_files):
            for se in src_env_files:
                if se.stem == "env":
                    env_files.append(se)
            for e in env_active or []:
                env_files.extend([se for se in src_env_files if se.stem == "env-{0}".format(e)])

        server_path = pathlib.Path(__file__).parent
        scan_env_files(list(server_path.glob("env*")))
        scan_env_files(list(self.root_path.glob("env*")))
        scan_env_files(list(server_path.joinpath("config").glob("env*")))
        return yaml_util.YamlPropertySourceLoader(env_files).load(env_extra)

    @staticmethod
    def set_common_argument(parser: argparse.ArgumentParser):
        parser.add_argument('-n', '--namespace', type=str)
        parser.add_argument('-p', '--param', nargs="+", default=[], type=lambda s: s.split("=", 1) if "=" in s else (s, ""), help="k1=v1 k2=v2")
        parser.add_argument('--env-active', nargs="+", default=[], help="list of env active")
        parser.add_argument('--ignore-namespace', action="store_true")
        parser.add_argument('--create-namespace', action="store_true")
        parser.add_argument('--roles', nargs="+", default=[])
        parser.add_argument('--debug', action="store_true", help="enable verbose output")
        parser.add_argument('--clean', action="store_true", help="clean build")
        parser.add_argument('--dry-run', action="store_true", help="only print not submit")
        parser.add_argument('--parallel', type=int, nargs='?', const=8, default=1)

    @staticmethod
    def __get_sub_parser_common_attr(name):
        return {
            "prog": "{0} {1}".format(os.path.basename(sys.argv[0]), name),
            "name": name,
            "usage": "%(prog)s [options]",
            "formatter_class": ArgParseHelpFormatter,
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
        parser.add_argument('--check', action="store_true")
        parser.add_argument('--proxy', action="store_true")
        parser.add_argument('--build-args', nargs="+", default=[])
        parser.add_argument('--tag')
        parser.add_argument('--push', action="store_true")

    def __init_backup_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.backup.value))
        self.set_common_argument(parser)

    def __init_restore_parser(self):
        parser = self.__command_parser.add_parser(**self.__get_sub_parser_common_attr(Command.restore.value))
        self.set_common_argument(parser)

    def run(self, **kwargs):
        self.__command_parser = self.arg_parser.add_subparsers(title="commands", metavar="", dest="command", required=True)
        self.__init_install_parser()
        self.__init_delete_parser()
        self.__init_build_parser()
        self.__init_backup_parser()
        self.__init_restore_parser()
        args: argparse.Namespace = self.arg_parser.parse_args()
        args.param = dict(args.param)
        logger.info("args: {0}".format(json.dumps(vars(args), indent=2)))
        if args.debug:
            logger.setLevel(logging.DEBUG)
        if args.clean:
            for t in filter(lambda a: a.is_dir(), self.root_path.rglob('build')):
                shutil.rmtree(t, ignore_errors=True)
                logger.debug(f'removed {t.as_posix()}')
        global_env = self.load_env_file(args.env_active, args.param)
        global_env["param_command"] = args.command
        jinja2ignore_rules = file_util.read_text(self.jinja2ignore_file).split("\n") if self.jinja2ignore_file and self.jinja2ignore_file.exists() else []
        roles = select_roles(self.root_path, self.role_deep, args)

        def process(r):
            role_build_path = r.role_path.joinpath("build")
            role_build_path.mkdir(parents=True, exist_ok=True)
            role_out_path = role_build_path.joinpath("out")
            role_doc_path = role_build_path.joinpath("doc")
            role_tmp_path = r.role_path.joinpath(".tmp")
            role_bak_path = role_tmp_path.joinpath("bak")
            role_env_file = r.role_path.joinpath("env.yml")
            role_env = {} | global_env | {
                "param_namespace": r.namespace,
                "param_role_name": r.role_name,
                "param_role_path": r.role_path.as_posix(),
                "param_role_tmp_path": role_tmp_path.as_posix(),
                "param_role_bak_path": role_bak_path.as_posix(),
                "param_role_build_path": role_build_path.as_posix(),
                "param_role_out_path": role_out_path.as_posix(),
                "param_role_doc_path": role_doc_path.as_posix()
            }
            logger.info(r.role_path.as_posix())
            if args.command == Command.backup.value:
                role_bak_path.mkdir(parents=True, exist_ok=True)
            # process env
            if role_env_file and role_env_file.exists():
                role_env |= yaml_util.load(template_util.Template(file_util.read_text(role_env_file)).render(**role_env))
            file_util.write_text(role_out_path.joinpath("env.yml"), yaml_util.dump(role_env))
            role_env |= args.param
            # process template
            for t in filter(lambda f: f.is_file() and not any(regex_util.match_rules(["build/", ".tmp/", role_env_file.name], f.as_posix()).values()), r.role_path.rglob("*")):
                _rules = regex_util.match_rules([*jinja2ignore_rules], t.as_posix())
                role_output_file = role_out_path.joinpath(t.relative_to(r.role_path))
                if not any(_rules.values()):
                    file_util.write_text(role_output_file, template_util.Template(file_util.read_text(t)).render(**role_env), t.stat().st_mode)
                else:
                    file_util.copy(t, role_output_file)
            role_context = RoleContext(
                *r,
                args=args,
                role_env=role_env,
                role_node_path=role_out_path / "node" / role_env.get("param_node_name", "null"),
                role_build_path=role_build_path,
                role_doc_path=role_doc_path,
                role_out_path=role_out_path,
            )
            role_instance = self.role_impl(context=role_context)
            if role_context.role_node_path.exists():
                path_util.merge_dir(role_context.role_node_path, role_context.role_out_path, role_instance.get_merge_ignore_pattern())

            # collect command
            _cmds = []
            if args.command == Command.build.value and args.target == "build.sh":
                target_file = role_out_path.joinpath(args.target)
                if target_file.exists():
                    _cmds.append("bash {0} {1}".format(target_file.as_posix(), " ".join(args.build_args)))

            _cmds.extend(getattr(role_instance, args.command)())
            any_doc_exclude = lambda a: not any(regex_util.match_rules(role_env["param_doc_excludes"] or [], a.as_posix()).values())
            if args.command == Command.build.name and args.target == 'doc' and any_doc_exclude(role_out_path):
                shutil.rmtree(role_doc_path, ignore_errors=True)
                file_util.sync(role_out_path, any_doc_exclude, role_doc_path)
                role_role_readme = role_out_path.joinpath("README.md")
                file_util.write_text(role_build_path.joinpath("doc.md"), role_instance.role_doc_content + "\n" + (file_util.read_text(role_role_readme) if role_role_readme.exists() else ""))
            execute(collection_util.flat_to_str(_cmds, delimiter=" && "), dry_run=args.dry_run)

        if args.parallel > 1:
            with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                list(executor.map(process, roles))
        else:
            list(map(process, roles))