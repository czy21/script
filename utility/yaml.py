import pathlib
from typing import Union

import yaml
from yaml import FullLoader

from utility import file as file_util, safe as safe_util, path as path_util


def join_tag(loader: FullLoader, node):
    args = loader.construct_sequence(node, deep=True)
    return args[0].join([args[i] for i in range(len(args)) if i != 0])


yaml.add_constructor('!join', join_tag)
yaml.add_constructor('!decrypt', lambda loader, node: safe_util.decrypt(*loader.construct_sequence(node, deep=True)))
yaml.add_constructor('!htpasswd', lambda loader, node: safe_util.htpasswd(*loader.construct_sequence(node, deep=True)))
yaml.add_constructor("!join_path", lambda loader, node: path_util.join_path(*loader.construct_sequence(node, deep=True)))


def load(stream: Union[str, pathlib.Path]) -> dict:
    return yaml.full_load(stream if isinstance(stream, str) else file_util.read_text(stream))
