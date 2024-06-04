import logging
from abc import abstractmethod
from typing import TypeVar, Generic

import jinja2.defaults

from utility import template as template_util

logger = logging.getLogger()

T = TypeVar('T')


class PropertySource(Generic[T]):
    name = None
    source: T = None

    def __init__(self, name, source: T):
        self.name = name
        self.source = source

    @abstractmethod
    def getProperty(self, name: str):
        pass

    @abstractmethod
    def getPropertyNames(self):
        pass


class PropertySourcesPlaceholdersResolver:
    sources: list[PropertySource[T]] = None
    extra: dict = None

    def __init__(self, sources, extra):
        self.sources = sources
        self.extra = extra

    def resolve_placeholder(self, source, name, value):
        sources = [r.source for r in self.sources]
        if self.extra:
            sources.insert(0, self.extra)
        for s in sources:
            resolved = template_util.Template(value, undefined=template_util.Undefined).render(**s)
            if jinja2.defaults.VARIABLE_START_STRING not in resolved:
                exec(name + "=resolved", locals(), source.source)
                return
