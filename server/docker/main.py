#!/usr/bin/env python3
import argparse
import pathlib

import share


def invoke(role_title: str, role_path: pathlib.Path, role_env_dict: dict, args: argparse.Namespace, **kwargs):
    cluster_name = role_env_dict.get("param_cluster_name")
    role_name = role_path.name
    role_conf_path = role_path.joinpath("conf")
    role_deploy_file = role_path.joinpath("deploy.yml")
    role_docker_file = role_path.joinpath("Dockerfile")
    role_init_sh = role_path.joinpath("init.sh")

    target_app_path = pathlib.Path(role_env_dict.get("param_docker_data")).joinpath(role_name)

    _cmds = []

    role_node_path = role_path.joinpath("node")
    role_node_target_path = next(filter(lambda a: str(a.name) == cluster_name, role_node_path.glob("*")), None) if role_node_path.exists() else None
    role_node_deploy_file = None
    if role_node_path.exists():
        if role_node_target_path:
            role_node_deploy_file = role_node_target_path.joinpath("deploy.yml")
            _cmds.append(share.role_print(role_title, "copy node", cluster_name))
            _cmds.append("find {0} -maxdepth 1 ! -path {0} ! -name deploy.yml -exec cp -rv -t {1}/".format(role_node_target_path.as_posix(), role_path.as_posix()) + " {} \\;")

    def docker_compose_cmd(option):
        role_deploy_files = [
            kwargs.get("base_deploy_file"),
            role_deploy_file.as_posix()
        ]
        if role_node_deploy_file and role_node_deploy_file.exists():
            role_deploy_files.append(role_node_deploy_file)
        return 'sudo docker-compose --project-name {0} {1} {2}'.format(role_name, " ".join(["--file {0}".format(t) for t in role_deploy_files]), option)

    if args.install:
        if role_conf_path.exists():
            target_role_conf_path = target_app_path.joinpath("conf")
            if target_role_conf_path.exists() and target_app_path.name == role_name:
                role_conf_relative_files = set(share.get_files(role_conf_path, role_path.as_posix()))
                if role_node_target_path and role_node_target_path.exists():
                    role_node_target_conf_relative_files = share.get_files(role_node_target_path.joinpath("conf"), role_node_target_path.as_posix())
                    role_conf_relative_files = role_conf_relative_files.union(role_node_target_conf_relative_files)
                remove_conf_files = [t.as_posix() for t in filter(lambda a: a.is_file(), target_role_conf_path.rglob("*")) if not any([t.as_posix().__contains__(s) for s in role_conf_relative_files])]
                if remove_conf_files:
                    _cmds.append(share.role_print(role_title, "remove conf"))
                    _cmds.append("sudo rm -rfv {0}".format(" ".join(remove_conf_files)))
            _cmds.append(share.role_print(role_title, "copy conf"))
            _cmds.append('sudo mkdir -p {1} && sudo cp -rv {0} {1}'.format(role_conf_path.as_posix(), target_app_path.as_posix()))
        if role_init_sh.exists():
            _cmds.append(share.role_print(role_title, "init", role_init_sh.as_posix()))
            _cmds.append("source {}".format(role_init_sh.as_posix()))
        if role_deploy_file.exists():
            _cmds.append(share.role_print(role_title, "deploy", role_deploy_file.as_posix()))
            if args.debug:
                _cmds.append(docker_compose_cmd("config"))
            _cmds.append(docker_compose_cmd(share.flat_to_str("up --detach --build --remove-orphans")))
    if args.delete:
        if role_deploy_file.exists():
            _cmds.append(share.role_print(role_title, "down", role_deploy_file.as_posix()))
            _cmds.append(docker_compose_cmd("down --remove-orphans"))

    if args.build_file == "Dockerfile":
        registry_url = role_env_dict['param_registry_url']
        registry_dir = role_env_dict['param_registry_dir']
        registry_username = role_env_dict['param_registry_username']
        registry_password = role_env_dict['param_registry_password']
        _cmds.append(share.role_print(role_title, "build", role_docker_file.as_posix()))
        _cmds.append('sudo docker login {0} --username {1} --password {2}'.format(registry_url, registry_username, registry_password))
        if role_docker_file.exists():
            docker_image_tag = "/".join([str(p).strip("/") for p in [registry_url, registry_dir, role_name]])
            _cmds.append("docker build --tag {0} --file {1} {2}".format(docker_image_tag, role_docker_file.as_posix(), role_path.as_posix()))
            _cmds.append("docker push {0}".format(docker_image_tag))
    _cmd_str = share.flat_to_str([_cmds, "echo \n"], delimiter=" && ")
    share.run_cmd(_cmd_str)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke, role_deep=2)
    installer.run(base_deploy_file=root_path.joinpath("base-deploy.yml"))
