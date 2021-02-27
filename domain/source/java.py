#!/usr/bin/env python3
import inspect
import json
import subprocess

from script.domain.default import common as default_common
from script.domain.source import base as base_source
from script.utility import basic as basic_util, collection as list_util, path as path_util, log

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_extra_config():
    base_source.build_by_template(default_common.param_api_extra_config_template_path, default_common.param_api_extra_config_output_file_path)
    logger.info(basic_util.action_formatter(__get_function_name(), default_common.param_api_extra_config_output_file_path))


def build_override_yml():
    base_source.build_by_template(default_common.param_api_yml_override_template_path, default_common.param_api_yml_output_file_path)
    logger.info(basic_util.action_formatter(__get_function_name(), default_common.param_api_yml_output_file_path))


def build_api_dockerfile():
    base_source.build_by_template(default_common.param_api_dockerfile_template_path, default_common.param_api_dockerfile_output_file_path)
    logger.info(basic_util.action_formatter(__get_function_name(), default_common.param_api_dockerfile_output_file_path))


def build_api_compose_file():
    base_source.build_by_template(default_common.param_api_compose_template_path, default_common.param_api_compose_output_file_path)
    logger.info(basic_util.action_formatter(__get_function_name(), default_common.param_api_compose_output_file_path))


def build_api():
    build_extra_config()
    command = list_util.arr_param_to_str(
        default_common.param_api_docker_gradle_command,
        [
            path_util.pure_path_join(default_common.param_api_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.pure_path_join(default_common.param_api_root_project_path, "build.gradle"),
            "--project-prop extraConfig=" + default_common.param_api_extra_config_output_file_path,
            "clean build -x test"
        ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
    build_override_yml()


def down_container() -> None:
    command = list_util.arr_param_to_str([
        "sudo docker-compose",
        "--file",
        default_common.param_api_compose_output_file_path,
        "--project-name",
        "_".join([default_common.param_project_name, default_common.param_env_suffix]),
        "down"
    ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(cmd=command)


def docker_images():
    proc = subprocess.Popen('sudo docker images --format "{{.Repository}}:{{.Tag}}"', stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    images = [x.strip() for x in proc.stdout.readlines() if x.strip()]
    proc.stdout.close()
    proc.wait()
    return images, proc


def rm_image(image_tag: str) -> None:
    images, proc = docker_images()
    if image_tag in images:
        command = list_util.arr_param_to_str(["docker", "image", "rmi", image_tag])
        logger.info(basic_util.action_formatter(__get_function_name(), command))
        basic_util.execute(cmd=command)


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


def build_api_compose():
    build_api_dockerfile()
    build_api_compose_file()


def start_api_compose():
    rm_image(default_common.param_api_image)
    command = list_util.arr_param_to_str(
        [
            "sudo docker-compose",
            "--file",
            default_common.param_api_compose_output_file_path,
            "--project-name",
            "_".join([default_common.param_project_name, default_common.param_env_suffix]),
            "up -d --build"
        ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def ensure_network():
    inspect_command = list_util.arr_param_to_str([
        "sudo docker network inspect",
        default_common.param_api_network_name,
    ])
    logger.info(basic_util.action_formatter(__get_function_name(), inspect_command))

    pre_connected_containers, proc = inspect_network(inspect_command)
    if proc.returncode == 1:
        create_network_command = list_util.arr_param_to_str(
            [
                "sudo docker network create",
                default_common.param_api_network_name
            ]
        )
        logger.info(basic_util.action_formatter(__get_function_name(), create_network_command))
        basic_util.execute(create_network_command)
    disconnect_command = " && ".join([
        list_util.arr_param_to_str("sudo docker network disconnect", default_common.param_api_network_name, d) for d in pre_connected_containers
    ])

    connect_command = " && ".join([
        list_util.arr_param_to_str("sudo docker network connect", default_common.param_api_network_name, d) for d in default_common.param_api_network_containers
    ])

    if disconnect_command:
        logger.info(basic_util.action_formatter(__get_function_name(), disconnect_command))
        basic_util.execute(disconnect_command)

    if connect_command:
        logger.info(basic_util.action_formatter(__get_function_name(), connect_command))
        basic_util.execute(connect_command)
    post_connected_containers, proc = inspect_network(inspect_command)
    logger.info(basic_util.action_formatter(__get_function_name(), "connected_containers: " + ",".join(post_connected_containers)))


def inspect_network(inspect_command):
    proc = subprocess.Popen(inspect_command, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    connected_containers = [v["Name"] for v in json.loads("".join([x.strip() for x in proc.stdout.readlines() if x.strip()]))[0]["Containers"].values()]
    proc.stdout.close()
    proc.wait()
    return connected_containers, proc


if __name__ == '__main__':
    print("ss")
