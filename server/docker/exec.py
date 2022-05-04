#!/usr/bin/env python3
import argparse
import pathlib
import re

import jinja2
import share


def invoke(role_title: str, role_path: pathlib.Path, **kwargs):
    args = kwargs["args"]
    env_dict: dict = kwargs["env_dict"]

    role_node_path = role_path.joinpath("node")
    role_node_selected = share.get_dir_dict(role_node_path) if role_node_path.exists() else None
    role_node_target_path: pathlib.Path = role_node_selected.get(next(iter(role_node_selected))) if role_node_selected else None
    if role_node_path.exists():
        if role_node_target_path:
            share.execute_cmd(share.flat_to_str([
                share.role_print(role_title, "copy node"),
                "cp -rv {0}/* {1}".format(role_node_target_path.as_posix(), role_path.as_posix())
            ], delimiter=" && "), select_tip="node option(example:1")
        else:
            return
    role_name = role_path.name
    role_conf_path = role_path.joinpath("conf")
    role_compose_file = role_path.joinpath("deploy.yml")
    role_docker_file = role_path.joinpath("Dockerfile")
    role_init_sh = role_path.joinpath("init.sh")
    role_build_sh = role_path.joinpath("build.sh")

    target_app_path = pathlib.Path(env_dict["param_docker_data"]).joinpath(role_name)
    for t in filter(lambda f: f.is_file() and share.exclude_match(args.exclude_pattern, f.as_posix()), role_path.rglob("*")):
        print(t)
        with open(t, "r", encoding="utf-8", newline="\n") as r_file:
            content = jinja2.Template(r_file.read()).render(**env_dict)
            with open(t, "w", encoding="utf-8") as t_file:
                t_file.write(content)

    def docker_compose_cmd(option):
        return 'sudo docker-compose --file {0} {1}'.format(role_compose_file.as_posix(), option)

    _cmds = []

    if args.i:
        if role_conf_path.exists():
            _cmds.append([
                share.role_print(role_title, "copy conf"),
                'sudo mkdir -p {0}'.format(target_app_path),
                'sudo cp -rv {0} {1}'.format(role_conf_path.as_posix(), target_app_path.as_posix())
            ])
        if role_init_sh.exists():
            _cmds.append([
                share.role_print(role_title, "init", role_init_sh.as_posix()),
                "source {}".format(role_init_sh.as_posix())
            ])
        if role_compose_file.exists():
            docker_up_options = [
                "up --detach --build --remove-orphans",
            ]
            if args.force_recreate:
                docker_up_options.append("--force-recreate")
            _cmds.append(share.role_print(role_title, "deploy", role_compose_file.as_posix()))
            if args.debug:
                _cmds.append(docker_compose_cmd("config"))
            _cmds.append(docker_compose_cmd(share.flat_to_str(docker_up_options)))
    if args.d:
        if role_compose_file.exists():
            _cmds.append([
                share.role_print(role_title, "down", role_compose_file.as_posix()),
                docker_compose_cmd("down --remove-orphans")
            ])

    if args.b:
        registry_url = env_dict['param_registry_url']
        registry_dir = env_dict['param_registry_dir']
        registry_username = env_dict['param_registry_username']
        registry_password = env_dict['param_registry_password']
        build_cmd = [
            share.role_print(role_title, "build", role_build_sh.as_posix()),
            'sudo docker login {0} --username {1} --password {2}'.format(registry_url, registry_username, registry_password)
        ]

        if role_docker_file.exists():
            docker_tag = "/".join([str(p).strip("/") for p in [registry_url, registry_dir, role_name]])
            build_cmd.append([
                "docker build --tag {0} --file {1} {2}".format(docker_tag, role_docker_file.as_posix(), role_path.as_posix()),
                "docker push {0}".format(docker_tag)
            ])
        if role_build_sh.exists():
            build_cmd.append(
                "sudo bash {0}".format(role_build_sh.as_posix())
            )
        if role_docker_file.exists() or role_build_sh.exists():
            _cmds.append(build_cmd)
    _cmd_str = share.flat_to_str([_cmds, "echo \n"], delimiter=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    env_file = pathlib.Path(__file__).parent.joinpath(".env").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('--force-recreate', action="store_true")
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
    share.execute(selected_option, invoke, env_file=env_file, args=args)
