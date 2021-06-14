#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def get_install_tuple(join_path):
    app_paths = [p for p in Path(__file__).parent.joinpath(join_path).iterdir() if p.is_dir()]
    for i, p in enumerate(app_paths, start=1):
        print(" ".join([str(i), p.name]))
    app_options = input("please select app number(example:1 2 3) ").strip().split()
    return [(int(t), app_paths.__getitem__(int(t) - 1)) for t in app_options if t in [str(i) for i, p in enumerate(app_paths, start=1)]]


def select_one_option():
    list_dir = [p for p in Path(__file__).parent.iterdir() if p.is_dir()]

    print("\n==========")

    for i, p in enumerate(list_dir, start=1):
        print(" ".join([str(i), p.name]))

    one_option = input("please select one option(example:1) ").strip()

    if one_option == '':
        return []

    elif not one_option.isnumeric():
        print("\ninvalid option")
        sys.exit()

    one_option = int(one_option)

    if not one_option in [i for i, p in enumerate(list_dir, start=1)]:
        print(" ".join(["\n", one_option, "not exist"]))
        sys.exit()
    return list_dir[one_option - 1]


def execute(app_tuples, func):
    for t in app_tuples:
        app_number = str(t[0])
        source_path = t[1]
        source_name = Path(source_path).name
        source_conf_path = Path(source_path).joinpath("conf")
        source_compose_file = Path(source_path).joinpath("deploy.yaml")

        source_init_config_sh = Path(source_path).joinpath("init_config.sh")
        source_post_config_sh = Path(source_path).joinpath("post_config.sh")
        app_id = " ".join([app_number, source_name])
        func(app_id,
             source_name,
             source_compose_file,
             source_conf_path,
             source_init_config_sh,
             source_post_config_sh
             )


def init_start(app_id, app_name, source_compose_file: Path, source_conf_path, source_init_config_sh, source_post_config_sh):
    if source_compose_file.exists():
        execute_shell(" ".join(['echo -e "{}\033[32m deploy => \033[0m {}"'.format(app_id, source_compose_file.as_posix()),
                                '&& kubectl apply -f {} '.format(source_compose_file.as_posix())
                                ]))
    execute_shell("echo \n")


def post_config(app_id, app_name, source_compose_file, source_conf_path, source_init_config_sh, source_post_config_sh):
    if source_post_config_sh.exists():
        execute_shell(" ".join(['echo -e "{}\033[32m post_config \033[0m => {}"'.format(app_id, source_post_config_sh.as_posix()),
                                '&& sudo bash', source_post_config_sh.as_posix()
                                ]))


def execute_shell(cmd: str):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    while True:
        output = proc.stdout.readline()
        if output == '' and proc.poll() is not None:
            break
        if output:
            print(output.strip())
    proc.stdout.close()
    proc.wait()


if __name__ == '__main__':
    global_env_file = Path(__file__).parent.joinpath(".env.global").as_posix()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action="store_true")
    parser.add_argument('-c', action="store_true")
    args = parser.parse_args()

    with open(global_env_file, "r") as e:
        global_env = dict((t.strip().split("=")[0], t.strip().split("=")[1]) for t in e)

        for t in global_env:
            global_env[t] = subprocess.getoutput(" ".join([
                "source " + global_env_file,
                "&& echo ${" + t + "}"
            ]))
    selected_init_option = select_one_option()
    if selected_init_option:
        selected_init_install = get_install_tuple(Path(selected_init_option).name)
        execute(selected_init_install, init_start)

    selected_post_option = select_one_option()
    if selected_post_option:
        selected_post_install = get_install_tuple(Path(selected_post_option).name)
        execute(selected_post_install, post_config)
