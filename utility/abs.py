import logging
from abc import abstractmethod
from typing import TypeVar, Generic

import jinja2.defaults
import pydash.objects

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

    def __init__(self, sources):
        self.sources = sources

    def resolve_placeholder(self, source, name, value):
        for s in self.sources:
            resolved = template_util.Template(value, undefined=template_util.Undefined).render(**s.source)
            if jinja2.defaults.VARIABLE_START_STRING not in resolved:
                pydash.objects.set_with(source.source, name, resolved)
                return
