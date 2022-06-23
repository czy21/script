#!/usr/bin/env python3
import argparse
import importlib
import importlib.util
import importlib.machinery
import io
import json
import os
import pathlib
import sys
from pathlib import Path

from utility import log as log_util, basic as basic_util, path as path_util

sys.path.append(pathlib.Path(__file__).parent.parent.as_posix())


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
    logger = log_util.Logger(__name__)

    env_path = Path(args.env).resolve()
    env_stem = env_path.parent.stem

    log_file = os.environ.run_args.log_file
    if log_file is not None:
        open(env_path.joinpath("../", log_file).resolve().as_posix(), 'w').close()

    # empty source log
    default_path_module = importlib.import_module("domain.default.path")
    getattr(default_path_module, "re_mkdir")(rm_output=args.init)

    # injected param to global
    env_pwd_mod = importlib.import_module("".join(["shell.", env_stem, "._env"]))
    env_common_mod = env_pwd_mod.env_common
    default_common_mod = importlib.import_module("domain.default.common")
    env_output_json = path_util.pure_path_join(getattr(default_path_module, "output"), "env.json")

    if args.init:
        env_common_mod.__dict__.update(dict({k: v for k, v in env_pwd_mod.__dict__.items() if k.startswith("param")}).items(), **param_input_dict)
        default_common_mod.__dict__.update(dict({k: v for k, v in env_common_mod.__dict__.items() if k.startswith("param")}))
        default_common_param = dict({k: v for k, v in default_common_mod.__dict__.items() if k.startswith("param")})
        env_json = json.dumps(default_common_param, sort_keys=True, indent=2)
        with io.open(env_output_json, "w+", encoding="utf-8") as f:
            f.write(env_json)
        logger.info(basic_util.action_formatter("params", env_json), default_common_mod.__name__)
    else:
        with io.open(env_output_json, 'r') as f:
            default_common_mod.__dict__.update(json.load(f))
    if args.cmd:
        exec(args.cmd)


if __name__ == '__main__':
    exec_file()
