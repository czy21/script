#!/usr/bin/env python3
import logging

from domain.default import common as default_common
from utility import basic as basic_util, collection as list_util

logger = logging.getLogger()


def build_api():
    command = list_util.flat_to_str([
        "cp -r",
        default_common.param_api_root_project_path + "/*",
        default_common.param_api_output_path
    ])
    basic_util.execute(command)
