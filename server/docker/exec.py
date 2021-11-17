#!/usr/bin/env python3
import argparse
import share
from pathlib import Path
from dotenv import dotenv_values


def execute(app_tuples, func, **kwargs):
    for t in app_tuples:
        app_number = str(t[0])
        source_path = t[1]
        source_name = Path(source_path).name
        app_id = " ".join([app_number, source_name])
        func(app_id, source_name, source_path, **kwargs)


def apply(app_id: str, app_name: str, source_path: Path, **kwargs):
    args = kwargs["args"]
    env_file = kwargs["env_file"]
    source_env_file = Path(source_path).joinpath(".env")
    source_conf_path = Path(source_path).joinpath("conf")
    source_compose_file = Path(source_path).joinpath("docker-compose.yml")
    env_values = {
        **dotenv_values(env_file),
        **{
            "param_role_name": app_name
        }
    }
    with open(source_env_file, "w+", encoding="utf-8") as f:
        f.write(u'{}'.format("\n".join(["=".join([k, v]) for (k, v) in env_values.items()])))

    source_init_sh = Path(source_path).joinpath("init.sh")
    source_build_sh = Path(source_path).joinpath("build.sh")

    target_app_path = Path(env_values["param_docker_data"]).joinpath(app_name)
    target_conf_path = target_app_path.joinpath("conf")

    if args.i:
        if source_conf_path.exists():
            share.execute_cmd("&&".join([
                'echo -e "{}\033[32m conf dir copy \033[0m"'.format(app_id),
                'sudo mkdir -p {}'.format(target_app_path),
                'sudo cp -rv {} {}'.format(source_conf_path.as_posix(), target_app_path.as_posix())
            ]))
        if source_init_sh.exists():
            share.execute_cmd("&&".join([
                'echo -e "{}\033[32m init.sh \033[0m => {}"'.format(app_id, source_init_sh.as_posix()),
                'sudo bash {}'.format(source_init_sh.as_posix())
            ]))
        if source_compose_file.exists():
            action = lambda a: 'sudo docker-compose --file {} --env-file {} {}'.format(source_compose_file.as_posix(), source_env_file, a)
            share.execute_cmd("&&".join([
                'echo -e "{}\033[32m docker-compose file => \033[0m {}"'.format(app_id, source_compose_file.as_posix()),
                action("config"),
                action("up --detach --build")
            ]))
    share.execute_cmd("echo \n")

    if args.b:
        if source_build_sh.exists():
            share.execute_cmd("&&".join([
                'echo -e "{}\033[32m build.sh \033[0m => {}"'.format(app_id, source_build_sh.as_posix()),
                'sudo docker login {} --username {} --password {}'.format(env_values['param_registry_url'], env_values['param_registry_username'], env_values['param_registry_password']),
                'sudo bash {}'.format(source_build_sh.as_posix())
            ]))
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
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    execute(selected_option["list"], apply, env_file=env_file, args=args)
    if args.p:
        share.execute_cmd("docker image prune --force --all")
