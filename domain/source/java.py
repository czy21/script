#!/usr/bin/env python3
import inspect

from script.domain.default import common as default_common
from script.utility import basic as basic_util, collection as list_util, path as path_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_api():
    build_method = ["clean", "build"]
    if default_common.param_api_module_name:
        build_method = [default_common.param_api_module_name + ":" + b for b in build_method]
    build_command = list_util.arr_param_to_str(
        [
            path_util.pure_path_join(default_common.param_api_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path if default_common.param_api_gradle_init_script_file_path else "",
            "--build-file " + path_util.pure_path_join(default_common.param_api_root_project_path, "build.gradle"),
            build_method,
            "-x test"
        ])
    logger.info(basic_util.action_formatter(__get_function_name(), build_command))
    basic_util.execute(build_command)


def build_plugin(publish_task=None):
    command = list_util.arr_param_to_str(
        [
            path_util.pure_path_join(default_common.param_api_gradle_plugin_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.pure_path_join(default_common.param_api_gradle_plugin_root_project_path, "build.gradle"),
        ]
    )

    if publish_task:
        command = list_util.arr_param_to_str(command, publish_task)
    else:
        command = list_util.arr_param_to_str(command, "publishAllPublicationsToBuildRepository")
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
