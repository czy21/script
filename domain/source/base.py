#!/usr/bin/env python3
import inspect
import io
from pathlib import Path

from script.domain.default import common as default_common
from script.utility import basic as basic_util, collection as list_util, log
logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]
