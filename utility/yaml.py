import pathlib
from typing import Union

import pydash.objects

import yaml
from utility import file as file_util, safe as safe_util, path as path_util, collection as collection_util, template as template_util, basic as basic_util
from yaml import FullLoader


def join_tag(loader: FullLoader, node):
    args = loader.construct_sequence(node, deep=True)
    return args[0].join(args[1:])


def load(stream: Union[str, pathlib.Path]) -> dict:
    loader1 = FullLoader
    yaml.add_constructor('!join', join_tag, loader1)
    yaml.add_constructor('!decrypt', lambda loader, node: safe_util.decrypt(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor('!htpasswd', lambda loader, node: safe_util.htpasswd(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor("!join_path", lambda loader, node: path_util.join_path(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor("!get_uid", lambda loader, node: basic_util.getpwnam_uid(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor("!get_gid", lambda loader, node: basic_util.getpwnam_gid(*loader.construct_sequence(node, deep=True)), loader1)

    return yaml.load(stream if isinstance(stream, str) else file_util.read_text(stream), loader1)


# TODO
def process(source: dict[str, object]):
    result = collection_util.flat_dict(source)
    for key, value in result.items():
        if isinstance(value, str):
            value = template_util.Template(value).render(**source)
            pydash.objects.set_(source, key, value)
    print(source)
