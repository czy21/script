#!/usr/bin/env python3

import argparse
import pathlib

import share
from utility import (
    collection as collection_util,
    path as path_util
)


def get_cmds(role_title: str,
             role_name: str,
             role_path: pathlib.Path,
             role_output_path: pathlib.Path,
             role_env: dict,
             namespace: str,
             args: argparse.Namespace,
             **kwargs):
    role_node_name = role_env.get("param_cluster_name")
    role_conf_path = role_output_path.joinpath("conf")
    role_deploy_file = role_output_path.joinpath("deploy.yml")
    role_init_sh = role_output_path.joinpath("init.sh")

    target_app_path = pathlib.Path(role_env.get("param_docker_data")).joinpath(role_name)
    param_role_target_path = role_env.get("param_role_target_path")
    if param_role_target_path:
        target_app_path = pathlib.Path(param_role_target_path)
    role_node_path = role_output_path.joinpath("node")
    role_node_target_path = next(filter(lambda a: a.is_dir and str(a.name) == role_node_name, role_node_path.glob("*")),
                                 None) if role_node_path.exists() else None
    role_node_target_deploy_file = None
    role_node_target_conf_path = None
    if role_node_target_path:
        path_util.merge_dir(role_output_path, role_node_target_path, ["node", "deploy.yml"])
        role_node_target_conf_path = role_node_target_path.joinpath("conf")
        role_node_target_deploy_file = role_node_target_path.joinpath("deploy.yml")
    _cmds = []

    def docker_compose_cmd(option):
        role_deploy_files = [
            kwargs.get("base_deploy_file"),
            role_deploy_file.as_posix()
        ]
        if role_node_target_deploy_file and role_node_target_deploy_file.exists():
            role_deploy_files.append(role_node_target_deploy_file)
        role_project_name = role_env.get("param_role_project_name")
        return 'sudo docker-compose --project-name {0} {1} {2}'.format(
            role_project_name if role_project_name else role_name,
            " ".join(["--file {0}".format(t) for t in role_deploy_files]), option)

    if args.command == share.Command.install.value:
        if role_conf_path.exists() or (role_node_target_conf_path and role_node_target_conf_path.exists()):
            _cmds.append('sudo mkdir -p {1} && sudo cp -rv {0} {1}'.format(
                role_node_target_conf_path if role_node_target_conf_path and role_node_target_conf_path.exists() else role_conf_path.as_posix(),
                target_app_path.as_posix())
            )
        if role_init_sh.exists():
            _cmds.append("bash {}".format(role_init_sh.as_posix()))
        if role_deploy_file.exists():
            if args.debug:
                _cmds.append(docker_compose_cmd("config"))
            up_args = ["up --detach --build --remove-orphans"]
            if args.recreate:
                up_args.append("--force-recreate")
            _cmds.append(docker_compose_cmd(collection_util.flat_to_str(up_args)))
    if args.command == share.Command.delete.value:
        if role_deploy_file.exists():
            _cmds.append(docker_compose_cmd("down --remove-orphans"))

    if args.command == share.Command.build.value and args.target.startswith("Dockerfile"):
        target_file = role_output_path.joinpath(args.target)
        registry_url = role_env['param_registry_url']
        registry_dir = role_env['param_registry_dir']
        if target_file.exists():
            image_tag = "/".join([
                str(p).strip("/")
                for p in [registry_url, registry_dir, (role_name + ":" + args.tag if args.tag else role_name)]
            ])
            _cmds.append("docker build --tag {0} --file {1} {2} --pull".format(image_tag, target_file.as_posix(), role_output_path.as_posix()))
            if args.push:
                _cmds.append("docker push {0}".format(image_tag))
    return _cmds


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, get_cmds, role_deep=2)
    installer.run(base_deploy_file=root_path.joinpath("deploy.yml"))
