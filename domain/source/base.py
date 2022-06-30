#!/usr/bin/env python3
import inspect
import logging

from utility import log

logger = logging.getLogger()


def __get_function_name():
    return inspect.stack()[1][3]
