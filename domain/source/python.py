#!/usr/bin/env python3
import inspect

import docker

from script.domain.default import common as default_common, path as default_path
from script.domain.source import base as base_source
from script.utility import basic as basic_util, collection as list_util, path as path_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_api():
    command = list_util.arr_param_to_str([
        "cp -r",
        default_common.param_api_root_project_path + "/*",
        default_common.param_api_output_path
    ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def build_api_compose():
    base_source.build_api_dockerfile()
    base_source.build_api_compose_file()
