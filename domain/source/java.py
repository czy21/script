#!/usr/bin/env python3
import io
import os
from pathlib import Path

from script.domain.default import common as default_common, path as default_path
from script.utility import template, basic as basic_util, list as list_util, path as path_util, log

logger = log.Logger(__name__)


def build_by_template(template_name, output_path):
    output_name = Path(output_path).resolve().joinpath(os.path.basename(template_name)).as_posix()
    with io.open(template_name, "r", encoding="utf-8", newline="\n") as source_template:
        with io.open(output_name, "w+", encoding="utf-8", newline="\n") as target_output:
            target_output.write(template.StringTemplate(source_template.read() + "\n")
                                .safe_substitute(default_common.get_params()))
    return output_name


def build_extra_config():
    logger.info(basic_util.action_formatter(build_extra_config.__name__))
    return build_by_template(default_common.param_api_extra_config_template_name, default_path.output_tmp)


def build_override_yml():
    logger.info(basic_util.action_formatter(build_override_yml.__name__))
    return build_by_template(default_common.param_api_yml_override_template_name, default_common.param_api_output_resource_path)


def build_api_dockerfile():
    logger.info(basic_util.action_formatter(build_api_dockerfile.__name__))
    return build_by_template(default_common.param_api_dockerfile_template_name, default_common.param_api_dockerfile_output_file_path)


def build_api():
    output_extra_config_name = build_extra_config()

    command = list_util.arr_param_to_str(
        default_common.param_api_docker_gradle_command,
        [
            "gradle",
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.pure_path_join(default_common.param_api_root_project_path, "build.gradle"),
            "--project-prop extraConfig=" + output_extra_config_name,
            "clean build -x test"
        ])
    logger.info(basic_util.action_formatter(build_api.__name__, command))
    basic_util.execute(command)
    build_override_yml()


def build_api_image():
    output_dockerfile__name = build_api_dockerfile()
    command = list_util.arr_param_to_str(
        [
            "cd&&sudo docker build",
            "--build-arg JAR_FILE=."
            + path_util.pure_path_join(default_common.param_api_output_path, default_common.param_api_archive_file_name).replace(Path(default_path.root_path).parent.as_posix(),
                                                                                                                                 ""),
            "--tag erp:1.0.0",
            "--file",
            output_dockerfile__name,
            "."
        ])
    logger.info(basic_util.action_formatter(build_api_image.__name__, command))
    basic_util.execute(command)


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
    logger.info(basic_util.action_formatter(build_plugin.__name__, command))
    basic_util.execute(command)
