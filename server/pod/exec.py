#!/usr/bin/env python3
import subprocess
from pathlib import Path
import share


def execute(app_tuples, env_path, func):
    for t in app_tuples:
        app_number = str(t[0])
        source_path = Path(t[1])
        source_name = source_path.name
        app_id = " ".join([app_number, source_name])
        func(app_id, source_name, source_path, env_path, )


def apply(app_id, app_name, source_path: Path, env_path: Path):
    temp_all_in_one_path = source_path.joinpath("___temp/all_in_one.yaml")
    temp_all_in_one_path.parent.mkdir(parents=True, exist_ok=True)
    temp_all_in_one_path.touch()
    execute_shell(".".join(['echo -e "{}\033[32m deploy => \033[0m {}"'.format(app_id, app_name), '&& helm install {} -f {} {} --debug --dry-run > {} '.format(app_name, env_path.as_posix(), source_path.as_posix(), temp_all_in_one_path.as_posix())]))
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
    env_path = Path(__file__).parent.joinpath("env.yaml")
    selected_init_option = share.select_one_option()
    if selected_init_option:
        selected_init_install = share.get_install_tuple(Path(selected_init_option).name)
        execute(selected_init_install, env_path, apply)
