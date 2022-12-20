import pathlib
import typing

import yaml
from utility import collection as collection_util

if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent.joinpath("___temp/a.yaml"), encoding="utf-8") as f:
        a = yaml.full_load(f)
        b = collection_util.dict_render(a, key_filter_func=lambda t: t.__contains__("p5"), val_filter_func=lambda t: t.__contains__("p2"))
        print(a)
