#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path
import share


def execute(app_tuples, func, **kwargs):
    for t in app_tuples:
        app_number = str(t[0])
        source_path = Path(t[1])
        source_name = source_path.name
        app_id = " ".join([app_number, source_name])
        func(app_id, source_name, source_path, **kwargs)


def apply(app_id: str, app_name: str, source_path: Path, **kwargs):
    args = kwargs["args"]
    if args.m:
        manual_cmd = 'bash {}'.format(source_path.joinpath("manual.sh").as_posix())
        execute_shell("&&".join([
            manual_cmd,
            "echo \n"
        ]))
    if args.i:
        chart_path = source_path.joinpath("Chart.yaml")
        temp_all_in_one_path = source_path.joinpath("___temp/deploy.yaml")
        temp_all_in_one_path.parent.mkdir(parents=True, exist_ok=True)
        temp_all_in_one_path.touch()
        echo_cmd = 'echo -e "{}\033[32m deploy \033[0m"'.format(app_id)
        if chart_path.exists():
            helm_cmd = 'helm template --values {} {} --debug > {}'.format(env_path.as_posix(), source_path.as_posix(), temp_all_in_one_path.as_posix())
            kube_cmd = 'kubectl apply --filename={}'.format(temp_all_in_one_path)
            execute_shell("&&".join([
                echo_cmd,
                helm_cmd,
                kube_cmd,
                "echo \n"
            ]))
        else:
            for t in source_path.glob("*.yaml"):
                yaml = source_path.joinpath(t.name).as_posix()
                execute_shell(".".join(['echo -e "{}\033[32m deploy => \033[0m {}"'.format(app_id, yaml), '&& kubectl apply --filename={}'.format(yaml)]))


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
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action="store_true")
    parser.add_argument('-m', action="store_true")
    parser.add_argument('-d', action="store_true")
    args = parser.parse_args()
    selected_init_option = share.select_one_option()
    if selected_init_option:
        selected_init_install = share.get_install_tuple(Path(selected_init_option).name)
        execute(selected_init_install, apply, env_path=env_path, args=args)
