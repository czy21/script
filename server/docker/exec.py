#!/usr/bin/env python3
import argparse
import sys

import share
from pathlib import Path
from dotenv import dotenv_values
from urllib import parse


def execute(app_tuples, func, **kwargs):
    for t in app_tuples:
        app_number = str(t[0])
        role_path = t[1]
        role_title = ".".join([app_number, role_path.name])
        func(role_title, role_path, **kwargs)


def apply(role_title: str, role_path: Path, **kwargs):
    args = kwargs["args"]
    env_file = kwargs["env_file"]
    role_name = role_path.name
    role_env_file = role_path.joinpath(".env")
    role_conf_path = role_path.joinpath("conf")
    role_compose_file = role_path.joinpath("deploy.yml")
    env_values = {
        **dotenv_values(env_file),
        **{
            "param_role_name": role_name,
            "param_role_path": role_path.as_posix(),
        }
    }

    with open(role_env_file, "w+", encoding="utf-8") as f:
        f.write(u'{}'.format("\n".join(["=".join([k, v]) for (k, v) in env_values.items()])))

    source_init_sh = role_path.joinpath("init.sh")
    role_build_sh = role_path.joinpath("build.sh")

    target_app_path = Path(env_values["param_docker_data"]).joinpath(role_name)

    if args.i:
        if role_conf_path.exists():
            share.execute_cmd(share.arr_param_to_str(
                [
                    share.role_print(role_title, "copy conf"),
                    'sudo mkdir -p {}'.format(target_app_path),
                    'sudo cp -rv {} {}'.format(role_conf_path.as_posix(), target_app_path.as_posix())
                ], separator=" && "
            ))
        if source_init_sh.exists():
            share.execute_cmd(share.arr_param_to_str(
                [
                    share.role_print(role_title, "init", source_init_sh.as_posix()),
                    ["source {}".format(t) for t in [role_env_file, source_init_sh.as_posix()]],
                ], separator=" && "
            ))
        if role_compose_file.exists():
            def docker_compose_cmd(a): return 'sudo docker-compose --file {} --env-file {} {}'.format(role_compose_file.as_posix(), role_env_file, a)

            share.execute_cmd(share.arr_param_to_str(
                [
                    share.role_print(role_title, "deploy", role_compose_file.as_posix()),
                    docker_compose_cmd("config"),
                    docker_compose_cmd("up --detach --build")
                ], separator=" && "
            ))
    share.execute_cmd("echo \n")

    if args.b:
        registry_url = env_values['param_registry_url']
        registry_dir = env_values['param_registry_dir']
        registry_username = env_values['param_registry_username']
        registry_password = env_values['param_registry_password']
        build_cmd = [
            share.role_print(role_title, "build", role_build_sh.as_posix()),
            'sudo docker login {} --username {} --password {}'.format(registry_url, registry_username, registry_password)
        ]
        dockerfile = role_path.joinpath("Dockerfile")
        if dockerfile.exists():
            docker_tag = "/".join([str(p).strip("/") for p in [registry_url, registry_dir, role_name]])
            build_cmd.append([
                "docker build --tag {} --file {} {}".format(docker_tag, dockerfile.as_posix(), role_path.as_posix()),
                "docker push {}".format(docker_tag)
            ])
        if role_build_sh.exists():
            build_cmd.append(
                ["source {}".format(t) for t in [role_env_file.as_posix(), role_build_sh.as_posix()]]
            )
        if dockerfile.exists() or role_build_sh.exists():
            share.execute_cmd(share.arr_param_to_str(build_cmd, separator=" && "))
    share.execute_cmd("echo \n")


if __name__ == '__main__':
    env_file = Path(__file__).parent.joinpath(".env").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action="store_true")
    parser.add_argument('-b', action="store_true")
    parser.add_argument('-p', action="store_true")

    parser.add_argument("-t", default=2)
    parser.add_argument('-n')

    args = parser.parse_args()
    if args.p:
        share.execute_cmd("docker image prune --force --all")
        sys.exit()
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    execute(selected_option["list"], apply, env_file=env_file, args=args)
