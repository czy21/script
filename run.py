#!/usr/bin/env python3
import argparse
import importlib
import importlib.machinery
import importlib.util
import inspect
import json
import logging
import pathlib

from domain.source.base import ExecutionContext, EnhancedNamespace
from utility import log as log_util, file as file_util, yaml as yaml_util

logger = logging.getLogger()


def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--file', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--env-file', nargs="+", default=[])
    parser.add_argument('-p', '--param', nargs="+", default=[], type=lambda s: s.split("=", 1) if "=" in s else (s, ""), help="k1=v1 k2=v2")
    args = parser.parse_args()
    args.param = dict(args.param)

    log_util.init_logger(file=pathlib.Path(args.file).with_suffix(".log"))

    logger.info("args: {0}".format(json.dumps(vars(args), indent=2)))

    default_params = {}
    default_path_module = importlib.import_module("domain.default.path")
    getattr(default_path_module, "create_dir")()
    default_path_params = {name: value.as_posix() for name, value in inspect.getmembers(default_path_module) if isinstance(value, pathlib.Path)}
    default_params |= default_path_params
    default_params |= args.param
    project_params = yaml_util.YamlPropertySourceLoader([pathlib.Path(t).resolve() for t in args.env_file]).load(default_params)
    context = ExecutionContext(
        root_path=pathlib.Path(default_path_params["root_path"]),
        output_path=pathlib.Path(default_path_params["output_path"]),
        param=EnhancedNamespace(**project_params)
    )
    file_util.write_text(context.output_path.joinpath("env.yml"), yaml_util.dump(context.param.__dict__))
    exec(args.exec, globals(), {'context': context})


if __name__ == '__main__':
    execute()
