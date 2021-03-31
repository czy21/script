#!/usr/bin/env python3
import inspect
import io
from pathlib import Path

from script.utility.template import CustomTemplate
import docker

from script.domain.default import common as default_common
from script.utility import basic as basic_util, collection as list_util, log
from docker import errors

logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_by_template(template_name, output_path):
    Path(output_path).parent.mkdir(exist_ok=True, parents=True)
    content = CustomTemplate(filename=template_name).render(**dict({k: v for k, v in default_common.__dict__.items() if k.startswith("param")}))
    with io.open(output_path, "w+", encoding="utf-8", newline="\n") as target_output:
        target_output.write(content)


def build_template_dict():
    for k, v in default_common.param_template_output_dict.items():
        build_by_template(k, v)
        logger.info(basic_util.action_formatter(__get_function_name(), ":".join([k, v])))


def down_container() -> None:
    command = list_util.arr_param_to_str([
        "sudo docker-compose",
        "--file",
        default_common.param_api_compose_file_output_path,
        "--project-name",
        "_".join([default_common.param_project_name, default_common.param_env_suffix]),
        "down"
    ])
    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(cmd=command)


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
    for c in network["Containers"].values():
        c_name = c["Name"]
        client.api.disconnect_container_from_network(container=c_name, net_id=network_id)
        logger.info(basic_util.action_formatter(__get_function_name(), list_util.arr_param_to_str([c_name, "disconnected", "from", network_name])))

    for t in default_common.param_api_network_containers:
        client.api.connect_container_to_network(container=t, net_id=network_id)
        logger.info(basic_util.action_formatter(__get_function_name(), list_util.arr_param_to_str([t, "connected", "to", network_name])))

    post_network = client.api.inspect_network(default_common.param_api_network_name)
    logger.info(basic_util.action_formatter(__get_function_name(),
                                            list_util.arr_param_to_str([
                                                "network:" + network_name,
                                                "containers:", ",".join([c["Name"] for c in post_network["Containers"].values()])
                                            ]))
                )


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
    scales = [k.split("_")[-1] + "=" + v for k, v in default_common.__dict__.items() if k.startswith("param_api_compose_scale_")]

    command = list_util.arr_param_to_str(
        [
            "sudo docker-compose",
            "--file",
            default_common.param_api_compose_file_output_path,
            "--project-name",
            "_".join([default_common.param_project_name, default_common.param_env_suffix]),
            "up --detach --build",
            ["--scale", scales] if scales else []
        ]
    )

    logger.info(basic_util.action_formatter(__get_function_name(), command))
    basic_util.execute(command)
