#!/usr/bin/env python3
import inspect

from script.utility import log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]
