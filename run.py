#!/usr/bin/env python3
import argparse
import importlib.util
import inspect
import json
import logging
import pathlib

from domain.source.base import ExecutionContext, EnhancedNamespace
from utility import log as log_util, file as file_util, yaml as yaml_util

logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--file', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--env', required=True)
    parser.add_argument('-p', '--param', nargs="+", default=[], type=lambda s: s.split("=", 1) if "=" in s else (s, ""), help="k1=v1 k2=v2")
    args = parser.parse_args()
    args.param = dict(args.param)
    log_util.init_logger(file=pathlib.Path(args.file).with_suffix(".log"))

    shell_cwd = pathlib.Path(args.file).parent.resolve()

    logger.info("args: {0}".format(json.dumps(vars(args), indent=2)))
    env_files = [shell_cwd.joinpath("_env.yml")]
    env_file_active = shell_cwd.joinpath(f"_env-{args.env}.yml")
    if env_file_active.exists():
        env_files.append(env_file_active)
    default_params = {}
    default_path_module = importlib.import_module("domain.default.path")
    getattr(default_path_module, "create_dir")()
    default_path_params = {name: value.as_posix() for name, value in inspect.getmembers(default_path_module) if isinstance(value, pathlib.Path)}
    default_params |= default_path_params
    default_params |= args.param
    project_params = yaml_util.YamlPropertySourceLoader(env_files).load(default_params)
    context = ExecutionContext(
        root_path=pathlib.Path(default_path_params["root_path"]),
        output_path=pathlib.Path(default_path_params["output_path"]),
        param=EnhancedNamespace(**project_params)
    )
    file_util.write_text(context.output_path.joinpath("env.yml"), yaml_util.dump(context.param.__dict__))
    exec(args.exec, globals(), {'context': context})
