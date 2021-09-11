#!/usr/bin/env python3
import argparse
import subprocess
import sys
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
    source_conf_path = Path(source_path).joinpath("conf")
    source_compose_file = Path(source_path).joinpath("docker-compose.yml")

    source_init_sh = Path(source_path).joinpath("init.sh")
    source_post_sh = Path(source_path).joinpath("post.sh")
    source_build_sh = Path(source_path).joinpath("build.sh")

    target_conf_path = Path(env["GLOBAL_CONFIG_DIR"]).joinpath(app_name)

    if args.i:
        if source_conf_path.exists():
            execute_shell(" ".join(['echo -e "{}\033[32m conf dir copy \033[0m"'.format(app_id),
                                    '&& sudo mkdir -p ' + target_conf_path.as_posix(),
                                    '&& sudo cp -rv ', source_conf_path.as_posix() + "/*", target_conf_path.as_posix() + "/"
                                    ]))
        else:
            execute_shell(" ".join(['echo -e "{}\033[32m conf dir no exist \033[0m"'.format(app_id)]))
        if source_init_sh.exists():
            execute_shell(" ".join(['echo -e "{}\033[32m init.sh \033[0m => {}"'.format(app_id, source_init_sh.as_posix()),
                                    '&& sudo bash', source_init_sh.as_posix()
                                    ]))
        else:
            execute_shell(" ".join(['echo -e "{}\033[32m init.sh not exist \033[0m"'.format(app_id)]))

        if source_compose_file.exists():
            execute_shell(" ".join(['echo -e "{}\033[32m start_compose => \033[0m ${}"'.format(app_id, source_compose_file.as_posix()),
                                    '&& sudo /usr/local/bin/docker-compose --file {} --env-file {} up --detach --build'.format(source_compose_file.as_posix(), global_env_file)
                                    ]))
        else:
            execute_shell(" ".join(['echo -e "{}\033[32m build.sh not exist \033[0m"'.format(app_id)]))
        execute_shell("echo \n")

    if args.b:
        if source_build_sh.exists():
            execute_shell(" ".join(['echo -e "{}\033[32m build.sh \033[0m => {}"'.format(app_id, source_build_sh.as_posix()),
                                    '&& sudo bash', source_build_sh.as_posix()
                                    ]))
        else:
            execute_shell(" ".join(['echo -e "{}\033[32m build.sh not exist \033[0m"'.format(app_id)]))
        execute_shell("echo \n")

    if args.c:
        if source_post_sh.exists():
            execute_shell(" ".join(['echo -e "{}\033[32m post_config \033[0m => {}"'.format(app_id, source_post_sh.as_posix()),
                                    '&& sudo bash', source_post_sh.as_posix()
                                    ]))
        execute_shell("echo \n")


def execute_shell(cmd: str):
    cmd = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stderr=sys.stderr, stdout=sys.stdout, encoding="utf-8")
    cmd.communicate()


if __name__ == '__main__':
    global_env_file = Path(__file__).parent.joinpath(".env.global").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action="store_true")
    parser.add_argument('-c', action="store_true")
    parser.add_argument('-b', action="store_true")
    parser.add_argument('-p', action="store_true")
    parser.add_argument("-t", default=2)
    args = parser.parse_args()

    with open(global_env_file, "r") as e:
        global_env = dict((t.strip().split("=")[0], t.strip().split("=")[1]) for t in e)

        for t in global_env:
            global_env[t] = subprocess.getoutput(" ".join([
                "source " + global_env_file,
                "&& echo ${" + t + "}"
            ]))
    selected_option = share.select_option(int(args.t))
    execute(selected_option, apply, env=global_env, args=args)
    action_func = lambda a: execute(selected_option, a, args=args)
    if args.p:
        execute_shell("docker image prune --force --all")
