import json
import pathlib

import jinja2
import yaml

from utility import collection as collection_util

if __name__ == '__main__':
    env_file = pathlib.Path(__file__).parent.joinpath("env.yaml")
    with open(env_file, mode="r", encoding="utf-8") as f:
        all_vars = collection_util.flat_dict(yaml.full_load(f.read()))
        # for k, v in all_vars.items():
        #     v = jinja2.Template(str(v)).render(all_vars)
        #     all_vars[k] = v
        print(json.dumps(all_vars))
        print(all_vars["param_c[3].name"])
