#!/usr/bin/env python3
import inspect

from domain.default import common as default_common
from utility import basic as basic_util, collection as list_util, log, path as path_util

logger = logging.getLogger()


def __get_function_name():
    return inspect.stack()[1][3]


def build_web():
    command = list_util.flat_to_str([
        "nrm use taobao",
        "&& yarn --cwd " + default_common.param_web_root_project_path, "install",
        "&& yarn --cwd " + default_common.param_web_root_project_path, "build",
        "&& cp -r",
        path_util.join_path(default_common.param_web_root_project_path, "build") + "/*",
        default_common.param_web_output_path
    ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
