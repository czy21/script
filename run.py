#!/usr/bin/env python3
import argparse
import importlib
import importlib.machinery
import importlib.util
import logging
import os
import pathlib
import sys
from pathlib import Path

import yaml

from utility import log as log_util, file as file_util

sys.path.append(pathlib.Path(__file__).parent.parent.as_posix())

logger = logging.getLogger()


def exec_file():
    parser = argparse.ArgumentParser()
    parser.add_argument('--param', nargs="+", default=[])
    parser.add_argument('--init', action="store_true")
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--env', required=True)
    parser.add_argument('--log-file')
    parser.add_argument('--cmd')
    args = parser.parse_args()
    param_iter = iter(args.param)
    param_input_dict = dict(zip(param_iter, param_iter))
    os.environ.__setattr__("run_args", args)

    env_path = Path(args.env).resolve()
    env_stem = env_path.parent.stem

    log_file = os.environ.run_args.log_file
    log_util.init_logger(file=env_path.joinpath("../", log_file).absolute() if log_file is not None else None)

    # empty source log
    default_path_module = importlib.import_module("domain.default.path")

    # injected param to global
    env_pwd_mod = importlib.import_module("".join(["shell.", env_stem, "._env"]))
    env_common_mod = env_pwd_mod.env_common
    default_common_mod = importlib.import_module("domain.default.common")
    env_output_yaml = pathlib.Path(getattr(default_path_module, "output")).joinpath("env.yaml")

    if args.init:
        env_common_mod.__dict__.update(dict({k: v for k, v in env_pwd_mod.__dict__.items() if k.startswith("param")}).items(), **param_input_dict)
        default_common_mod.__dict__.update(dict({k: v for k, v in env_common_mod.__dict__.items() if k.startswith("param")}))
        default_common_param = dict({k: v for k, v in default_common_mod.__dict__.items() if k.startswith("param")})
        file_util.write_text(env_output_yaml, yaml.dump(default_common_param))
    else:
        default_common_mod.__dict__.update(yaml.full_load(file_util.read_text(env_output_yaml)))
    if args.cmd:
        exec(args.cmd)


if __name__ == '__main__':
    exec_file()
