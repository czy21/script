#!/usr/bin/env python3
import argparse
import pathlib

import share

from utility import (
    collection as collection_util,
    file as file_util
)


def invoke(role_title: str, role_path: pathlib.Path, role_env: dict, namespace: str, args: argparse.Namespace, **kwargs):
    cluster_name = role_env.get("param_cluster_name")
    role_name = role_path.name
    role_conf_path = role_path.joinpath("conf")
    role_deploy_file = role_path.joinpath("deploy.yml")
    role_init_sh = role_path.joinpath("init.sh")

    target_app_path = pathlib.Path(role_env.get("param_docker_data")).joinpath(role_name)
    param_role_target_path = role_env.get("param_role_target_path")
    if param_role_target_path:
        target_app_path = pathlib.Path(param_role_target_path)

    _cmds = []

    role_node_path = role_path.joinpath("node")
    role_node_target_path = next(filter(lambda a: str(a.name) == cluster_name, role_node_path.glob("*")), None) if role_node_path.exists() else None
    role_node_deploy_file = None
    if role_node_path.exists():
        if role_node_target_path:
            role_node_deploy_file = role_node_target_path.joinpath("deploy.yml")
            share.execute(collection_util.flat_to_str([
                share.echo_action(role_title, "copy node", cluster_name),
                "find {0} -maxdepth 1 ! -path {0} ! -name deploy.yml -exec cp -rv -t {1}/".format(role_node_target_path.as_posix(), role_path.as_posix()) + " {} \\;"
            ], delimiter=" && "), dry_run=args.dry_run)

    def docker_compose_cmd(option):
        role_deploy_files = [
            kwargs.get("base_deploy_file"),
            role_deploy_file.as_posix()
        ]
        if role_node_deploy_file and role_node_deploy_file.exists():
            role_deploy_files.append(role_node_deploy_file)
        role_project_name = role_env.get("param_role_project_name")
        return 'sudo docker-compose --project-name {0} {1} {2}'.format(role_project_name if role_project_name else role_name, " ".join(["--file {0}".format(t) for t in role_deploy_files]), option)

    if args.command == "install":
        if role_conf_path.exists():
            target_role_conf_path = target_app_path.joinpath("conf")
            if target_role_conf_path.exists() and target_app_path.name == role_name:
                role_conf_relative_files = set(file_util.get_files(role_conf_path, role_path.as_posix()))
                if role_node_target_path and role_node_target_path.exists():
                    role_node_target_conf_relative_files = file_util.get_files(role_node_target_path.joinpath("conf"), role_node_target_path.as_posix())
                    role_conf_relative_files = role_conf_relative_files.union(role_node_target_conf_relative_files)
                remove_conf_files = [t.as_posix() for t in filter(lambda a: a.is_file(), target_role_conf_path.rglob("*")) if not any([t.as_posix().__contains__(s) for s in role_conf_relative_files])]
                if remove_conf_files:
                    _cmds.append(share.echo_action(role_title, "remove conf"))
                    _cmds.append("sudo rm -rfv {0}".format(" ".join(remove_conf_files)))
            _cmds.append(share.echo_action(role_title, "copy conf"))
            _cmds.append('sudo mkdir -p {1} && sudo cp -rv {0} {1}'.format(role_conf_path.as_posix(), target_app_path.as_posix()))
        if role_init_sh.exists():
            _cmds.append(share.echo_action(role_title, "init", role_init_sh.as_posix()))
            _cmds.append("bash {}".format(role_init_sh.as_posix()))
        if role_deploy_file.exists():
            _cmds.append(share.echo_action(role_title, "deploy", role_deploy_file.as_posix()))
            if args.debug:
                _cmds.append(docker_compose_cmd("config"))
            up_args = ["up --detach --build --remove-orphans"]
            if args.recreate:
                up_args.append("--force-recreate")
            _cmds.append(docker_compose_cmd(collection_util.flat_to_str(up_args)))
    if args.command == "delete":
        if role_deploy_file.exists():
            _cmds.append(share.echo_action(role_title, "down", role_deploy_file.as_posix()))
            _cmds.append(docker_compose_cmd("down --remove-orphans"))

    if args.command == "build" and args.file and args.file.startswith("Dockerfile"):
        role_docker_file = role_path.joinpath(args.file)
        registry_url = role_env['param_registry_url']
        registry_dir = role_env['param_registry_dir']
        _cmds.append(share.echo_action(role_title, "build", role_docker_file.as_posix()))
        if role_docker_file.exists():
            docker_image_tag = "/".join([str(p).strip("/") for p in [registry_url, registry_dir, role_name + ("-" + args.tag if args.tag else "")]])
            _cmds.append("docker build --tag {0} --file {1} {2}".format(docker_image_tag, role_docker_file.as_posix(), role_path.as_posix()))
            _cmds.append("docker push {0}".format(docker_image_tag))
    _cmd_str = collection_util.flat_to_str(_cmds, delimiter=" && ")
    share.execute(_cmd_str, dry_run=args.dry_run)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke, role_deep=2)
    installer.run(base_deploy_file=root_path.joinpath("deploy.yml"))
