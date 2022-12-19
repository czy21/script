import pathlib
import typing

import yaml
from utility import collection as collection_util


def recursive_dict(data: dict, template_value_func: typing.Union[str, str]):
    for k, v in data.items():
        if isinstance(v, dict):
            recursive_dict(v, template_value_func)
        if isinstance(v, list):
            for i in range(len(v)):
                recursive_dict(v[i], template_value_func)


if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent.joinpath("___temp/a.yaml"), encoding="utf-8") as f:
        a = yaml.full_load(f)
        b = collection_util.dict_render(a)
        print(a)
