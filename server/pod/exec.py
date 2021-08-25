#!/usr/bin/env python3
import subprocess
import sys
from itertools import zip_longest
from pathlib import Path


def get_install_tuple(join_path):
    app_paths = [p for p in Path(__file__).parent.joinpath(join_path).iterdir() if p.is_dir()]
    # group by
    list_str = [list(t) for t in zip_longest(*[iter([".".join([str(i), p.name]) for i, p in enumerate(app_paths, start=1)])] * 8, fillvalue='')]
    # get every column max length
    column_widths = [len(max([t[p] for t in list_str for p in range(len(t)) if p == i], key=len, default='')) for i in range(len(list_str[0]))]
    for t in list_str:
        print("".join([str(t[p]).ljust(column_widths[o] + 2) for p in range(len(t)) for o in range(len(column_widths)) if p == o]))
    app_options = input("please select app number(example:1 2 3) ").strip().split()
    return [(int(t), app_paths.__getitem__(int(t) - 1)) for t in app_options if t in [str(i) for i, p in enumerate(app_paths, start=1)]]


def select_one_option():
    list_dir = [p for p in Path(__file__).parent.iterdir() if p.is_dir()]

    print("\n==========")
    for i, p in enumerate(list_dir, start=1):
        print(" ".join([str(i), p.name]))
    print("\n==========")
    one_option = input("please select one option(example:1) ").strip()

    if one_option == '':
        return []

    elif not one_option.isnumeric():
        print("\ninvalid option")
        sys.exit()

    one_option = int(one_option)

    if one_option not in [i for i, p in enumerate(list_dir, start=1)]:
        print(" ".join(["\n", one_option, "not exist"]))
        sys.exit()
    return list_dir[one_option - 1]


def execute(app_tuples, func):
    for t in app_tuples:
        app_number = str(t[0])
        source_path = Path(t[1])
        source_name = source_path.name
        app_id = " ".join([app_number, source_name])
        func(app_id, source_name, source_path)


def apply(app_id, app_name, source_path: Path):
    for t in source_path.glob("*.yaml"):
        yaml = source_path.joinpath(t.name).as_posix()
        execute_shell(" ".join(['echo -e "{}\033[32m deploy => \033[0m {}"'.format(app_id, yaml), '&& kubectl apply --filename={}'.format(yaml)]))
    execute_shell("echo \n")


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

    with open(global_env_file, "r") as e:
        global_env = dict((t.strip().split("=")[0], t.strip().split("=")[1]) for t in e)
        for t in global_env:
            global_env[t] = subprocess.getoutput(" ".join(["source " + global_env_file, "&& echo ${" + t + "}"]))
    selected_init_option = select_one_option()
    if selected_init_option:
        selected_init_install = get_install_tuple(Path(selected_init_option).name)
        execute(selected_init_install, apply)
