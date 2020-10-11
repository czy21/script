#!/usr/bin/env python3
import io
import os
from pathlib import Path

from script.domain.default import common as default_common, path as default_path
from script.utility import basic as basic_util, collection as list_util, path as path_util, log
from script.utility.template import CustomTemplate

logger = log.Logger(__name__)


def build_by_template(template_name, output_path):
    output_name = Path(output_path).resolve().joinpath(os.path.basename(template_name)).as_posix()
    content = CustomTemplate(filename=template_name).render(**default_common.get_params())
    with io.open(output_name, "w+", encoding="utf-8", newline="\n") as target_output:
        target_output.write(content)
    return output_name


def build_extra_config():
    config_path = build_by_template(default_common.param_api_extra_config_template_name, default_path.output_tmp)
    logger.info(basic_util.action_formatter(build_extra_config.__name__, config_path))
    return config_path


def build_override_yml():
    yml_path = build_by_template(default_common.param_api_yml_override_template_name, default_common.param_api_output_resource_path)
    logger.info(basic_util.action_formatter(build_override_yml.__name__, yml_path))
    return yml_path


def build_api_dockerfile():
    dockerfile_path = build_by_template(default_common.param_api_dockerfile_template_name, default_common.param_api_dockerfile_output_file_path)
    logger.info(basic_util.action_formatter(build_api_dockerfile.__name__, dockerfile_path))
    return dockerfile_path


def build_api_compose_file():
    compose_file_path = build_by_template(default_common.param_api_compose_template_name, default_common.param_api_compose_output_file_path)
    logger.info(basic_util.action_formatter(build_api_compose_file.__name__, compose_file_path))
    return compose_file_path


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


def rm_container(image_tag: str) -> None:
    command = list_util.arr_param_to_str([
        "docker rm -f",
        "$(docker ps --filter",
        "ancestor=" + image_tag,
        "-q)"
    ])
    logger.info(basic_util.action_formatter(rm_container.__name__, command))
    basic_util.execute(cmd=command, ignore_error=True)


def rm_image(image_tag: str) -> None:
    command = list_util.arr_param_to_str(["docker", "image", "rmi", image_tag])
    logger.info(basic_util.action_formatter(rm_image.__name__, command))
    basic_util.execute(cmd=command, ignore_error=True)


def build_api_image():
    output_dockerfile__name = build_api_dockerfile()
    param_injected = default_common.get_params()["param_injected"]
    image_tag = ":".join([param_injected["param_project_name"], param_injected["param_api_image_tag"]])
    command = list_util.arr_param_to_str(
        [
            "cd && sudo docker build",
            "--build-arg",
            list_util.arr_param_to_str([
                "JAR_FILE=."
                + path_util.pure_path_join(default_common.param_api_output_path,
                                           default_common.param_api_archive_file_name).replace(Path(default_path.root_path).parent.as_posix(), ""),
                "JAR_RESOURCES=."
                + path_util.pure_path_join(default_common.param_api_output_resource_path).replace(Path(default_path.root_path).parent.as_posix(), ""),
            ], ","),
            "--tag " + image_tag,
            "--file", output_dockerfile__name,
            "."
        ])
    rm_container(image_tag)
    rm_image(image_tag)
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


def start_api_compose():
    output_compose_name = build_api_compose_file()
    command = list_util.arr_param_to_str(
        [
            "sudo docker-compose",
            "--file",
            output_compose_name,
            "up -d"
        ])
    logger.info(basic_util.action_formatter(start_api_compose.__name__, command))
    basic_util.execute(command)
