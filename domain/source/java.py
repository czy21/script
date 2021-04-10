#!/usr/bin/env python3
import inspect
import os

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
    build_command = list_util.arr_param_to_str(
        [
            path_util.pure_path_join(default_common.param_api_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.pure_path_join(default_common.param_api_root_project_path, "build.gradle"),
            "--project-prop extraConfig=" + default_common.param_api_gradle_extra_config_output_path,
            "clean build -x test"
        ])
    if default_common.param_api_docker_gradle_command:
        client = docker.from_env()
        os.system("chmod +x " + path_util.pure_path_join(default_common.param_api_root_project_path, "gradlew"))
        gradle_container = client.containers.run(image="gradle:jdk11",
                                                 command=list_util.arr_param_to_str(build_command),
                                                 volumes=[
                                                     ":".join([default_path.root_path, default_path.root_path]),
                                                     ":".join([path_util.pure_path_join(default_path.root_path, ".gradle"), "/home/gradle/.gradle"])
                                                 ],
                                                 remove=True,
                                                 stream=True
                                                 )
        for line in gradle_container:
            logger.info(basic_util.action_formatter(__get_function_name(), line.decode("utf-8").strip()))
    else:
        logger.info(basic_util.action_formatter(__get_function_name(), build_command))
        basic_util.execute(build_command)


def build_plugin(publish_task=None):
    command = list_util.arr_param_to_str(
        default_common.param_api_docker_gradle_command,
        [
            "gradle",
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + default_common.param_api_plugin_file_path,
        ]
    )

    if publish_task:
        command = list_util.arr_param_to_str(command, publish_task)
    else:
        command = list_util.arr_param_to_str(command, "publishAllPublicationsToBuildRepository")
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
