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
    return [(int(t), app_paths.__getitem__(int(t) - 1)) for t in app_options if t.isnumeric() and t in [str(i) for i, p in enumerate(app_paths, start=1)]]


def select_one_option():
    list_dir = [p for p in Path(__file__).parent.iterdir() if p.is_dir()]

    print("\n==========")

    for i, p in enumerate(list_dir, start=1):
        print(" ".join([str(i), p.name]))

    one_option = input("please select one option(example:1) ").strip()
    if not one_option.isnumeric():
        print("\ninvalid option")
        sys.exit()

    one_option = int(one_option)

    if not one_option in [i for i, p in enumerate(list_dir, start=1)]:
        print(" ".join(["\n", one_option, "not exist"]))
        sys.exit()
    return list_dir[one_option - 1]


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
    option_name = select_one_option()
    install_tuple = get_install_tuple(Path(option_name).name)
    for t in install_tuple:
        app_number = str(t[0])
        source_path = t[1]
        source_name = Path(source_path).name
        source_conf_path = Path(source_path).joinpath("conf")

        source_init_config_sh = Path(source_path).joinpath("init_config.sh")
        source_post_config_sh = Path(source_path).joinpath("post_config.sh")

        target_conf_path = Path(global_env["GLOBAL_CONFIG_DIR"]).joinpath(source_name)
        app_id = " ".join([app_number, source_name])
        if source_conf_path.exists():
            subprocess.call(args=" ".join(['echo -e "{}\033[32m conf dir copy \033[0m"'.format(app_id),
                                           '&& sudo mkdir -p ' + target_conf_path.as_posix(),
                                           '&& sudo cp -rv ', source_conf_path.as_posix() + "/*", target_conf_path.as_posix() + "/"
                                           ]), shell=True)
        else:
            subprocess.call(args=" ".join(['echo -e "{}\033[32m conf dir no exist \033[0m"'.format(app_id)]), shell=True)

        if source_init_config_sh.exists():
            subprocess.call(args=" ".join(['echo -e "{}\033[32m init_config \033[0m => {}"'.format(app_id, source_init_config_sh.as_posix()),
                                           '&& sudo bash', source_init_config_sh.as_posix()
                                           ]), shell=True)
        else:
            subprocess.call(args=" ".join(['echo -e "{}\033[32m init_config not exist \033[0m"'.format(app_id)]), shell=True)
