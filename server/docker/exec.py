#!/usr/bin/env python3
import argparse
import sys

import jinja2
import share
from pathlib import Path
from dotenv import dotenv_values


def execute(app_tuples, func, **kwargs):
    for t in app_tuples:
        app_number = str(t[0])
        role_path = t[1]
        role_title = ".".join([app_number, role_path.name])
        func(role_title, role_path, **kwargs)


def invoke(role_title: str, role_path: Path, **kwargs):
    args = kwargs["args"]
    env_file = kwargs["env_file"]
    role_name = role_path.name
    role_env_file = role_path.joinpath(".env")
    role_conf_path = role_path.joinpath("conf")
    role_compose_file = role_path.joinpath("deploy.yml")
    role_docker_file = role_path.joinpath("Dockerfile")
    role_init_sh = role_path.joinpath("init.sh")
    role_build_sh = role_path.joinpath("build.sh")

    env_values = {
        **dotenv_values(env_file),
        **{
            "param_role_name": role_name,
            "param_role_path": role_path.as_posix(),
        }
    }
    target_app_path = Path(env_values["param_docker_data"]).joinpath(role_name)

    for t in role_path.rglob("*"):
        if t.is_file():
            with open(t, "r", encoding="utf-8", newline="\n") as c_conf:
                content = jinja2.Template(c_conf.read()).render(**env_values)
                with open(t, "w", encoding="utf-8") as t_conf:
                    t_conf.write(content)

    if args.i:
        if role_conf_path.exists():
            share.execute_cmd(share.arr_param_to_str(
                [
                    share.role_print(role_title, "copy conf"),
                    'sudo mkdir -p {0}'.format(target_app_path),
                    'sudo cp -rv {0} {1}'.format(role_conf_path.as_posix(), target_app_path.as_posix())
                ], separator=" && "
            ))
        if role_init_sh.exists():
            share.execute_cmd(share.arr_param_to_str(
                [
                    share.role_print(role_title, "init", role_init_sh.as_posix()),
                    ["source {}".format(t) for t in [role_env_file, role_init_sh.as_posix()]],
                ], separator=" && "
            ))
        if role_compose_file.exists():
            def docker_compose_cmd(a): return 'sudo docker-compose --file {0} {1}'.format(role_compose_file.as_posix(), a)

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
                ["source {0}".format(t) for t in [role_env_file.as_posix(), role_build_sh.as_posix()]]
            )
        if role_docker_file.exists() or role_build_sh.exists():
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
    execute(selected_option["list"], invoke, env_file=env_file, args=args)
