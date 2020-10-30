#!/usr/bin/env python3
import inspect

from script.domain.default import common as default_common
from script.domain.source import base as base_source
from script.utility import basic as basic_util, collection as list_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_web():
    command = list_util.arr_param_to_str([
        "nrm use taobao && cd",
        default_common.param_web_root_project_path,
        "&& yarn install && yarn build && cp -r build/*",
        default_common.param_web_output_path
    ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def build_cp_shell():
    base_source.build_by_template(default_common.param_web_cp_template_path, default_common.param_web_cp_output_file_path)
    logger.info(basic_util.action_formatter(__get_function_name(), default_common.param_web_cp_output_file_path))
