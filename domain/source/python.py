#!/usr/bin/env python3
import inspect

from script.domain.default import common as default_common
from script.utility import basic as basic_util, collection as list_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_api():
    command = list_util.flat_to_str([
        "cp -r",
        default_common.param_api_root_project_path + "/*",
        default_common.param_api_output_path
    ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
