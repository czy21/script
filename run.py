#!/usr/bin/env python3
import argparse
import importlib
import importlib.machinery
import importlib.util
import inspect
import logging
import pathlib
import sys
from types import SimpleNamespace

from domain.source.base import ExecutionContext, EnhancedNamespace
from utility import log as log_util, file as file_util, yaml as yaml_util

sys.path.append(pathlib.Path(__file__).parent.parent.as_posix())

logger = logging.getLogger()


def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--file', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--env-file', nargs="+", default=[])
    args = parser.parse_args()

    log_util.init_logger(file=pathlib.Path(args.file).with_suffix(".log"))

    default_path_module = importlib.import_module("domain.default.path")
    default_path_params = {name: value.as_posix() for name, value in inspect.getmembers(default_path_module) if isinstance(value, pathlib.Path)}
    getattr(default_path_module, "create_dir")()
    env_param = yaml_util.YamlPropertySourceLoader([pathlib.Path(t).resolve() for t in args.env_file]).load(default_path_params)
    context = ExecutionContext(
        root_path=pathlib.Path(default_path_params["root_path"]),
        output_path=pathlib.Path(default_path_params["output_path"]),
        param=EnhancedNamespace(**env_param)
    )
    file_util.write_text(context.output_path.joinpath("env.yml"), yaml_util.dump(context.param))
    exec(args.exec, globals(), {'context': context})


if __name__ == '__main__':
    execute()
