#!/usr/bin/env python3
import argparse
import pathlib

import share


def invoke(role_title: str, role_path: pathlib.Path, **kwargs):
    args = kwargs["args"]
    env_dict: dict = kwargs["env_dict"]

    role_node_path = role_path.joinpath("node")
    role_node_selected = share.get_dir_dict(role_node_path, select_tip="node num(example:1)") if role_node_path.exists() else None
    role_node_target_path: pathlib.Path = role_node_selected.get(next(iter(role_node_selected))) if role_node_selected else None
    if role_node_path.exists():
        if role_node_target_path:
            share.execute_cmd(share.flat_to_str([
                share.role_print(role_title, "copy node"),
                "cp -rv {0}/* {1}".format(role_node_target_path.as_posix(), role_path.as_posix())
            ], delimiter=" && "))
        else:
            return
    role_name = role_path.name
    role_conf_path = role_path.joinpath("conf")
    role_compose_file = role_path.joinpath("deploy.yml")
    role_docker_file = role_path.joinpath("Dockerfile")
    role_init_sh = role_path.joinpath("init.sh")
    role_build_sh = role_path.joinpath("build.sh")

    target_app_path = pathlib.Path(env_dict["param_docker_data"]).joinpath(role_name)

    def docker_compose_cmd(option):
        return 'sudo docker-compose --project-name {0} --file {1} --file {2} {3}'.format(role_name, kwargs["base_deploy_file"], role_compose_file.as_posix(), option)

    _cmds = []

    if args.i:
        if role_conf_path.exists():
            _cmds.append(share.role_print(role_title, "copy conf"))
            _cmds.append('sudo mkdir -p {0}'.format(target_app_path))
            _cmds.append('sudo cp -rv {0} {1}'.format(role_conf_path.as_posix(), target_app_path.as_posix()))
        if role_init_sh.exists():
            _cmds.append(share.role_print(role_title, "init", role_init_sh.as_posix()))
            _cmds.append("source {}".format(role_init_sh.as_posix()))
        if role_compose_file.exists():
            _cmds.append(share.role_print(role_title, "deploy", role_compose_file.as_posix()))
            if args.debug:
                _cmds.append(docker_compose_cmd("config"))
            _cmds.append(docker_compose_cmd(share.flat_to_str("up --detach --build --remove-orphans")))
    if args.d:
        if role_compose_file.exists():
            _cmds.append(share.role_print(role_title, "down", role_compose_file.as_posix()))
            _cmds.append(docker_compose_cmd("down --remove-orphans"))

    if args.b:
        registry_url = env_dict['param_registry_url']
        registry_dir = env_dict['param_registry_dir']
        registry_username = env_dict['param_registry_username']
        registry_password = env_dict['param_registry_password']
        _cmds.append(share.role_print(role_title, "build", role_build_sh.as_posix()))
        _cmds.append('sudo docker login {0} --username {1} --password {2}'.format(registry_url, registry_username, registry_password))
        if role_docker_file.exists():
            docker_image_tag = "/".join([str(p).strip("/") for p in [registry_url, registry_dir, role_name]])
            _cmds.append("docker build --tag {0} --file {1} {2}".format(docker_image_tag, role_docker_file.as_posix(), role_path.as_posix()))
            _cmds.append("docker push {0}".format(docker_image_tag))
        if role_build_sh.exists():
            _cmds.append("sudo bash {0}".format(role_build_sh.as_posix()))
    _cmd_str = share.flat_to_str([_cmds, "echo \n"], delimiter=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    env_file = root_path.joinpath("env.yaml").as_posix()
    base_deploy_file = root_path.joinpath("base-deploy.yml").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", default=[])
    parser.add_argument('-i', action="store_true")
    parser.add_argument('-d', action="store_true")
    parser.add_argument('-b', action="store_true")
    parser.add_argument('-n')
    parser.add_argument('--debug', action="store_true")

    args = parser.parse_args()
    selected_option = share.select_option(2)
    if args.n is None:
        args.n = selected_option["namespace"]
    share.execute(selected_option, invoke, root_path=root_path.as_posix(), env_file=env_file, base_deploy_file=base_deploy_file, args=args)
