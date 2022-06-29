import json
import pathlib

import jinja2
import pydash
import yaml

from utility import collection as collection_util,yaml as yaml_util

if __name__ == '__main__':
    env_file = pathlib.Path(__file__).parent.joinpath("env.yaml")
    print(yaml.full_load("param_a:a"))
    # yaml_util.load(env_file)
    # with open(env_file, mode="r", encoding="utf-8") as f:
    #     all_vars = collection_util.dict_render(yaml.full_load(f.read()))
    #     print(json.dumps(all_vars, indent=1))
