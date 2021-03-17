#!/usr/bin/env python3
import inspect
import json
import subprocess
import docker

from script.domain.default import common as default_common, path as default_path
from script.domain.source import base as base_source
from script.utility import basic as basic_util, collection as list_util, path as path_util, log
from docker import errors
from docker.models.configs import Config
from compose import project, config

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
    build_command = list_util.arr_param_to_str(
        [
            path_util.pure_path_join(default_common.param_api_root_project_path, "gradlew"),
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.pure_path_join(default_common.param_api_root_project_path, "build.gradle"),
            "--project-prop extraConfig=" + default_common.param_api_extra_config_output_file_path,
            "clean build -x test"
        ])
    if default_common.param_api_docker_gradle_command:
        client = docker.from_env()
        gradle_container = client.containers.run(image="gradle:jdk11",
                                                 command=build_command,
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
    build_override_yml()


def down_container() -> None:
    ppp = config.config.ConfigFile.from_filename(default_common.param_api_compose_output_file_path)

    project.Project.from_config(name="_".join([default_common.param_project_name, default_common.param_env_suffix]), config_data=ppp, client=docker.from_env()).down()
    print("sss")
    # command = list_util.arr_param_to_str([
    #     "sudo docker-compose",
    #     "--file",
    #     default_common.param_api_compose_output_file_path,
    #     "--project-name",
    #     "_".join([default_common.param_project_name, default_common.param_env_suffix]),
    #     "down"
    # ])
    # logger.info(basic_util.action_formatter(__get_function_name(), command))
    # basic_util.execute(cmd=command)


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
    client = docker.from_env()
    try:
        client.api.remove_image(default_common.param_api_image)
    except errors.ImageNotFound:
        logger.info(basic_util.action_formatter(__get_function_name(),
                                                list_util.arr_param_to_str([
                                                    "image:" + default_common.param_api_image, " not found"
                                                ]))
                    )

    command = list_util.arr_param_to_str(
        [
            "sudo docker-compose",
            "--file",
            default_common.param_api_compose_output_file_path,
            "--project-name",
            "_".join([default_common.param_project_name, default_common.param_env_suffix]),
            "up -d --build"
        ]
    )
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)


def ensure_network():
    client = docker.from_env()
    try:
        client.networks.get(default_common.param_api_network_name)
    except errors.NotFound:
        client.api.create_network(name=default_common.param_api_network_name, driver="bridge")
        logger.info(basic_util.action_formatter(__get_function_name(), list_util.arr_param_to_str(["created network:", default_common.param_api_network_name])))
    network = client.api.inspect_network(default_common.param_api_network_name)
    network_id = network["Id"]
    network_name = network["Name"]
    network_containers = network["Containers"]
    for c in network_containers.values():
        c_name = c["Name"]
        client.api.disconnect_container_from_network(container=c_name, net_id=network_id)
        logger.info(basic_util.action_formatter(__get_function_name(), list_util.arr_param_to_str([c_name, "disconnected", "from", network_name])))

    for t in default_common.param_api_network_containers:
        client.api.connect_container_to_network(container=t, net_id=network_id)
        logger.info(basic_util.action_formatter(__get_function_name(), list_util.arr_param_to_str([t, "connected", "to", network_name])))

    logger.info(basic_util.action_formatter(__get_function_name(),
                                            list_util.arr_param_to_str([
                                                "network:" + network_name,
                                                "containers:", ",".join([c["Name"] for c in network_containers.values()])
                                            ]))
                )


if __name__ == '__main__':
    print("ss")
