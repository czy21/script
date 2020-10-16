#!/usr/bin/env python3
import io
import subprocess

from script.domain.default import common as default_common
from script.utility import basic as basic_util, collection as list_util, path as path_util, log
from script.utility.template import CustomTemplate

logger = log.Logger(__name__)


def build_by_template(template_name, output_path):
    content = CustomTemplate(filename=template_name).render(**default_common.get_params())
    with io.open(output_path, "w+", encoding="utf-8", newline="\n") as target_output:
        target_output.write(content)


def build_extra_config():
    build_by_template(default_common.param_api_extra_config_template_path, default_common.param_api_extra_config_output_file_path)
    logger.info(basic_util.action_formatter(build_extra_config.__name__, default_common.param_api_extra_config_output_file_path))


def build_override_yml():
    build_by_template(default_common.param_api_yml_override_template_path, default_common.param_api_yml_output_file_path)
    logger.info(basic_util.action_formatter(build_override_yml.__name__, default_common.param_api_yml_output_file_path))


def build_api_dockerfile():
    build_by_template(default_common.param_api_dockerfile_template_path, default_common.param_api_dockerfile_output_file_path)
    logger.info(basic_util.action_formatter(build_api_dockerfile.__name__, default_common.param_api_dockerfile_output_file_path))


def build_api_compose_file():
    build_by_template(default_common.param_api_compose_template_path, default_common.param_api_compose_output_file_path)
    logger.info(basic_util.action_formatter(build_api_compose_file.__name__, default_common.param_api_compose_output_file_path))


def build_api():
    build_extra_config()
    command = list_util.arr_param_to_str(
        default_common.param_api_docker_gradle_command,
        [
            "gradle",
            "--init-script " + default_common.param_api_gradle_init_script_file_path,
            "--build-file " + path_util.pure_path_join(default_common.param_api_root_project_path, "build.gradle"),
            "--project-prop extraConfig=" + default_common.param_api_extra_config_output_file_path,
            "clean build -x test"
        ])
    logger.info(basic_util.action_formatter(build_api.__name__, command))
    basic_util.execute(command)
    build_override_yml()


def down_container(compose_file_command: str) -> None:
    command = list_util.arr_param_to_str(compose_file_command, "down")
    logger.info(basic_util.action_formatter(down_container.__name__, command))
    basic_util.execute(cmd=command)


def rm_image(image_tag: str) -> None:
    command = list_util.arr_param_to_str(["docker", "image", "rmi", image_tag])
    logger.info(basic_util.action_formatter(rm_image.__name__, command))
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
    logger.info(basic_util.action_formatter(build_plugin.__name__, command))
    basic_util.execute(command)


def start_api_compose():
    build_api_dockerfile()
    build_api_compose_file()
    rm_image(default_common.param_api_image)
    command = list_util.arr_param_to_str(
        [
            "sudo docker-compose",
            "--file",
            default_common.param_api_compose_output_file_path,
            "up -d --build"
        ])
    logger.info(basic_util.action_formatter(start_api_compose.__name__, command))
    basic_util.execute(command)


def ensure_network():
    inspect_command = list_util.arr_param_to_str([
        "sudo docker network inspect",
        default_common.param_api_network_name,
        "--format '{{range $t :=.Containers}}{{$t.Name}},{{end}}'"
    ])
    logger.info(basic_util.action_formatter(ensure_network.__name__, inspect_command))

    pre_connected_containers, proc = inspect_network(inspect_command)
    if proc.returncode == 1:
        create_network_command = list_util.arr_param_to_str(
            [
                "sudo docker network create",
                default_common.param_api_network_name
            ]
        )
        logger.info(basic_util.action_formatter(ensure_network.__name__, create_network_command))
        basic_util.execute(create_network_command)
    connect_command = " && ".join([list_util.arr_param_to_str("sudo docker network connect", default_common.param_api_network_name, d)
                                   for d in list(set(default_common.param_api_network_containers).difference(set(pre_connected_containers)))])
    disconnect_command = " && ".join([list_util.arr_param_to_str("sudo docker network disconnect", default_common.param_api_network_name, d)
                                      for d in list(set(pre_connected_containers).difference(set(default_common.param_api_network_containers)))])
    if connect_command:
        logger.info(basic_util.action_formatter(ensure_network.__name__, connect_command))
        basic_util.execute(connect_command)
    if disconnect_command:
        logger.info(basic_util.action_formatter(ensure_network.__name__, disconnect_command))
        basic_util.execute(connect_command)
    post_connected_containers, proc = inspect_network(inspect_command)
    logger.info(basic_util.action_formatter(ensure_network.__name__, "connected_containers: " + ",".join(post_connected_containers)))


def inspect_network(inspect_command):
    proc = subprocess.Popen(inspect_command, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    connected_containers = [x.strip() for x in proc.stdout.readline().split(",") if x.strip()]
    proc.stdout.close()
    proc.wait()
    return connected_containers, proc

if __name__ == '__main__':
    print("ss")