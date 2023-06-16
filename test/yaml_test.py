import os.path
import pathlib
import typing

import jinja2
import yaml
from utility import yaml as yaml_util

if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent.joinpath("___temp/a.yaml"), encoding="utf-8") as f:
        a = yaml.full_load(f)
        yaml_util.process(a)
