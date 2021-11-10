#!/usr/bin/env python3
import argparse
import subprocess
import share
from pathlib import Path


def execute(app_tuples, func, **kwargs):
    for t in app_tuples:
        app_number = str(t[0])
        source_path = t[1]
        source_name = Path(source_path).name
        app_id = " ".join([app_number, source_name])
        func(app_id, source_name, source_path, **kwargs)


def apply(app_id: str, app_name: str, source_path: Path, **kwargs):
    args = kwargs["args"]
    env = kwargs["env"]
    env_file = kwargs["env_file"]
    source_conf_path = Path(source_path).joinpath("conf")
    source_compose_file = Path(source_path).joinpath("docker-compose.yml")

    source_init_sh = Path(source_path).joinpath("init.sh")
    source_post_sh = Path(source_path).joinpath("post.sh")
    source_build_sh = Path(source_path).joinpath("build.sh")

    target_app_path = Path(env["GLOBAL_DOCKER_DATA"]).joinpath(app_name)
    target_conf_path = target_app_path.joinpath("conf")
    target_data_path = target_app_path.joinpath("data")

    share.execute_cmd(" ".join([
        'echo -e "{}\033[32m create app dir \033[0m"'.format(app_id),
        '&& sudo mkdir -p ' + " ".join([target_app_path.as_posix(),target_conf_path.as_posix(),target_data_path.as_posix()])
    ]))
    if args.i:
        if source_conf_path.exists():
            share.execute_cmd(" ".join(['echo -e "{}\033[32m conf dir copy \033[0m"'.format(app_id),
                                    '&& sudo cp -rv ', source_conf_path.as_posix() + "/*", target_conf_path.as_posix() + "/"
                                    ]))
        else:
            share.execute_cmd(" ".join(['echo -e "{}\033[32m conf dir no exist \033[0m"'.format(app_id)]))
        if source_init_sh.exists():
            share.execute_cmd(" ".join(['echo -e "{}\033[32m init.sh \033[0m => {}"'.format(app_id, source_init_sh.as_posix()),
                                    '&& sudo bash', source_init_sh.as_posix()
                                    ]))
        else:
            share.execute_cmd(" ".join(['echo -e "{}\033[32m init.sh not exist \033[0m"'.format(app_id)]))

        if source_compose_file.exists():
            share.execute_cmd(" ".join(['echo -e "{}\033[32m start_compose => \033[0m {}"'.format(app_id, source_compose_file.as_posix()),
                                    '&& sudo /usr/local/bin/docker-compose --file {} --env-file {} up --detach --build'.format(source_compose_file.as_posix(), env_file)
                                    ]))
        else:
            share.execute_cmd(" ".join(['echo -e "{}\033[32m build.sh not exist \033[0m"'.format(app_id)]))
        share.execute_cmd("echo \n")

    if args.b:
        if source_build_sh.exists():
            share.execute_cmd(" ".join(['echo -e "{}\033[32m build.sh \033[0m => {}"'.format(app_id, source_build_sh.as_posix()),
                                    '&& sudo bash', source_build_sh.as_posix()
                                    ]))
        else:
            share.execute_cmd(" ".join(['echo -e "{}\033[32m build.sh not exist \033[0m"'.format(app_id)]))
        share.execute_cmd("echo \n")

    if args.c:
        if source_post_sh.exists():
            share.execute_cmd(" ".join(['echo -e "{}\033[32m post_config \033[0m => {}"'.format(app_id, source_post_sh.as_posix()),
                                    '&& sudo bash', source_post_sh.as_posix()
                                    ]))
        share.execute_cmd("echo \n")


if __name__ == '__main__':
    env_file = Path(__file__).parent.joinpath(".env.global").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action="store_true")
    parser.add_argument('-c', action="store_true")
    parser.add_argument('-b', action="store_true")
    parser.add_argument('-p', action="store_true")
    parser.add_argument("-t", default=2)
    with open(env_file, "r") as e:
        env = dict((t.strip().split("=")[0], t.strip().split("=")[1]) for t in e)
        for t in env:
            env[t] = subprocess.getoutput(" ".join([
                "source " + env_file,
                "&& echo ${" + t + "}"
            ]))
    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    parser.add_argument('-n', default=selected_option["namespace"])
    args = parser.parse_args()
    execute(selected_option["list"], apply, env=env, env_file=env_file, args=args)
    if args.p:
        share.execute_cmd("docker image prune --force --all")
