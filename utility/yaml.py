import logging
import pathlib
from typing import Union

import jinja2.defaults
import yaml

from utility import (
    file as file_util,
    safe as safe_util,
    path as path_util,
    collection as collection_util,
    basic as basic_util,
    abs
)

logger = logging.getLogger()


def join_tag(loader: yaml.FullLoader, node):
    args = loader.construct_sequence(node, deep=True)
    return args[0].join(args[1:])


def load(stream: Union[str, pathlib.Path]) -> dict:
    loader1 = yaml.FullLoader
    yaml.add_constructor('!join', join_tag, loader1)
    yaml.add_constructor('!decrypt', lambda loader, node: safe_util.decrypt(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor('!htpasswd', lambda loader, node: safe_util.htpasswd(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor("!join_path", lambda loader, node: path_util.join_path(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor("!get_uid", lambda loader, node: basic_util.getpwnam_uid(*loader.construct_sequence(node, deep=True)), loader1)
    yaml.add_constructor("!get_gid", lambda loader, node: basic_util.getpwnam_gid(*loader.construct_sequence(node, deep=True)), loader1)

    return yaml.load(stream if isinstance(stream, str) else file_util.read_text(stream), loader1)


def dump(data):
    return yaml.dump_all([data], None, Dumper=yaml.Dumper, sort_keys=False)


class OriginTrackedMapPropertySource(abs.PropertySource[dict]):
    flatten = None

    def __init__(self, name, source):
        super().__init__(name, source)
        self.flatten = collection_util.flat_dict(
            source,
            key_wrap_func=lambda key: "['{0}']".format(key),
            val_predicate=lambda val: val and isinstance(val, str) and jinja2.defaults.VARIABLE_START_STRING in val,
            value_empty=""
        )

    def getProperty(self, name: str):
        return self.flatten.get(name)

    def getPropertyNames(self):
        return self.flatten.keys()


class YamlPropertySourceLoader:
    file_extensions = ["yaml", "yml"]
    resources: list[pathlib.Path] = None

    def __init__(self, resources):
        self.resources = resources

    def load(self) -> dict:
        sources = []
        for r in self.resources:
            if r.suffix and r.suffix[1:] in self.file_extensions:
                sources.append(OriginTrackedMapPropertySource(r.as_posix(), load(r)))
        resolver = abs.PropertySourcesPlaceholdersResolver(sources)
        for t in sources:
            for name in t.getPropertyNames():
                resolver.resolve_placeholder(t, name, t.getProperty(name))
        d = {}
        for t in reversed(sources):
            logger.info("load env_file: %s" % t.name)
            d |= t.source
        return d
