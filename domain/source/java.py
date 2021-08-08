#!/usr/bin/env python3
import inspect
import os
from pathlib import Path

import docker

from script.domain.default import common as default_common, path as default_path
from script.domain.source import base as base_source
from script.utility import basic as basic_util, collection as list_util, path as path_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_extra_config():
    base_source.build_by_template(default_common.param_api_gradle_extra_config_template_path, default_common.param_api_gradle_extra_config_output_path)
    logger.info(basic_util.action_formatter(__get_function_name(), default_common.param_api_gradle_extra_config_output_path))


def build_api():
    build_extra_config()
    build_method = ["clean", "build"]
    if default_common.param_api_module_name:
        build_method = [default_common.param_api_module_name + ":" + b for b in build_method]
    build_command = list_util.arr_param_to_str(
        [
            path_util.pure_path_join(default_common.param_api_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.pure_path_join(default_common.param_api_root_project_path, "build.gradle"),
            "--project-prop extraConfig=" + default_common.param_api_gradle_extra_config_output_path,
            build_method,
            "-x test"
        ])
    logger.info(basic_util.action_formatter(__get_function_name(), build_command))
    basic_util.execute(build_command)


def copy_config():
    cp_cmd = list_util.arr_param_to_str(
        "mkdir -p",
        default_common.param_api_config_path,
        "&&"
        "cp -rv",
        default_common.param_api_config_output_path + "/*",
        default_common.param_api_config_path
    )
    logger.info(basic_util.action_formatter(__get_function_name(), cp_cmd))
    basic_util.execute(cp_cmd)


def build_plugin(publish_task=None):
    command = list_util.arr_param_to_str(
        default_common.param_api_docker_gradle_command,
        [
            "gradle",
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + default_common.param_api_gradle_plugin_file_path,
        ]
    )

    if publish_task:
        command = list_util.arr_param_to_str(command, publish_task)
    else:
        command = list_util.arr_param_to_str(command, "publishAllPublicationsToBuildRepository")
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
