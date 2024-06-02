import pathlib
import sys

import yaml

from utility import yaml as yaml_util

if __name__ == '__main__':
    env_paths = list(sorted(pathlib.Path(__file__).parent.joinpath("build").glob("**/env*.yaml"), reverse=False))
    propertySources = yaml_util.YamlPropertySourceLoader(env_paths).load()
    yaml.dump(propertySources, stream=sys.stdout,sort_keys=False)
    print("")
