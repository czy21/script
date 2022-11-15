#!/usr/bin/env python3
import logging

from domain.default import common as default_common
from utility import basic as basic_util, collection as list_util, path as path_util

logger = logging.getLogger()


def build_web():
    command = list_util.flat_to_str([
        "nrm use taobao",
        "&& yarn --cwd " + default_common.param_web_root_project_path, "install",
        "&& yarn --cwd " + default_common.param_web_root_project_path, "build",
        "&& cp -r",
        path_util.join_path(default_common.param_web_root_project_path, "build") + "/*",
        default_common.param_web_output_path
    ])
    basic_util.execute(command)
