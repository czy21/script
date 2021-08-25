#!/usr/bin/env python3
import subprocess
from pathlib import Path
import share

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
    selected_init_option = share.select_one_option()
    if selected_init_option:
        selected_init_install = share.get_install_tuple(Path(selected_init_option).name)
        execute(selected_init_install, apply)
