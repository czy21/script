#!/usr/bin/env python3
import os
import argparse
import json
import logging
import pathlib

from domain.base import ExecutionContext, EnhancedNamespace
from utility import log as log_util, file as file_util, yaml as yaml_util

logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--file', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--env-active', required=False)
    parser.add_argument('-p', '--param', nargs="+", default=[], type=lambda s: s.split("=", 1) if "=" in s else (s, ""), help="k1=v1 k2=v2")
    args = parser.parse_args()
    args.param = dict(args.param)
    log_util.init_logger(file=pathlib.Path(args.file).with_suffix(".log"))

    shell_cwd = pathlib.Path(args.file).parent.resolve()

    logger.info("args: {0}".format(json.dumps(vars(args), indent=2)))
    env_files = [shell_cwd.joinpath("_env.yml")]
    env_files.extend(filter(lambda f: f.exists(),[shell_cwd.joinpath(f"_env-{t}.yml") for t in (args.env_active or '').split(',')]))
    
    root_path = pathlib.Path(os.environ.get('root_path', pathlib.Path(__file__).joinpath("../../").resolve()))

    source_db = root_path / "db"
    version_file = root_path / "version"

    output_path = root_path / ".output"
    output_temp = output_path / "temp"
    output_db = output_path / "db"
    output_db_all = output_db / "all"
    output_db_bak = output_db / "bak"

    [p.mkdir(parents=True, exist_ok=True) for p in [output_temp, output_db_all, output_db_bak]]

    default_params = {
        'root_path': root_path,
        'source_db': source_db,
        'version_file': version_file,
        'output_path': output_path,
        'output_temp': output_temp,
        'output_db': output_db,
        'output_db_all': output_db_all,
        'output_db_bak': output_db_bak
    }
    default_params |= {k:v.as_posix() for k,v in default_params.items() if isinstance(v, pathlib.Path) }
    default_params |= args.param
    project_params = yaml_util.YamlPropertySourceLoader(env_files).load(default_params)
    context = ExecutionContext(root_path=root_path, output_path=output_path, param=EnhancedNamespace(**project_params))
    file_util.write_text(context.output_path.joinpath("env.yml"), yaml_util.dump(context.param.__dict__))
    exec(args.exec, globals(), {'context': context})
