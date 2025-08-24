#!/usr/bin/env python3
import abc
import logging
import pathlib
import typing
from types import SimpleNamespace

logger = logging.getLogger()


class EnhancedNamespace(SimpleNamespace):

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

class ExecutionContext(typing.NamedTuple):
    root_path: pathlib.Path
    output_path: pathlib.Path
    param: EnhancedNamespace

class AbstractSource(metaclass=abc.ABCMeta):
    def __init__(self, context: ExecutionContext) -> None:
        self.context = context
