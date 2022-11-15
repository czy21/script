#!/usr/bin/env python3
import logging

from domain.default import common as default_common
from utility import basic as basic_util, collection as list_util, path as path_util

logger = logging.getLogger()


def build_api():
    build_method = ["clean", "build"]
    if default_common.param_api_module_name:
        build_method = [default_common.param_api_module_name + ":" + b for b in build_method]
    build_command = list_util.flat_to_str(
        [
            path_util.join_path(default_common.param_api_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path if default_common.param_api_gradle_init_script_file_path else "",
            "--build-file " + path_util.join_path(default_common.param_api_root_project_path, "build.gradle"),
            build_method,
            "-x test"
        ])
    basic_util.execute(build_command)


def build_plugin(publish_task=None):
    command = list_util.flat_to_str(
        [
            path_util.join_path(default_common.param_api_gradle_plugin_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.join_path(default_common.param_api_gradle_plugin_root_project_path, "build.gradle"),
        ]
    )

    if publish_task:
        command = list_util.flat_to_str(command, publish_task)
    else:
        command = list_util.flat_to_str(command, "publishAllPublicationsToBuildRepository")
    basic_util.execute(command)
