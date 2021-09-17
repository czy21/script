#!/usr/bin/env python3
import argparse,io,subprocess
from pathlib import Path
from ruamel import yaml
import share


def _str_representer(dumper: yaml.Dumper, data):
    style = ''
    if '\n' in data:
        style = '|'
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style)

def execute(app_tuples, func, **kwargs):
    yaml.RoundTripRepresenter.add_representer(str, _str_representer)
    for t in app_tuples:
        app_number = str(t[0])
        source_path = Path(t[1])
        source_name = source_path.name
        app_id = " ".join([app_number, source_name])
        func(app_id, source_name, source_path, **kwargs)


def get_kube_cmd(action: str, yaml_path: str):
    return 'kubectl {} --filename={} '.format(action, yaml_path)


def apply(app_id: str, app_name: str, source_path: Path, **kwargs):
    args = kwargs["args"]
    kubectl_action = 'delete' if args.d else 'apply'

    temp_all_in_one_path = source_path.joinpath("___temp/deploy.yaml")
    temp_all_in_one_path.parent.mkdir(parents=True, exist_ok=True)
    temp_all_in_one_path.touch()
    echo_cmd = 'echo -e "{}\033[32m deploy\033[0m"'.format(app_id)
    kube_cmd = get_kube_cmd(kubectl_action, temp_all_in_one_path.as_posix())
    cmd_func = lambda x: 'bash -xc \'{}\''.format(x)
    cmd = [echo_cmd]

    helm_dep_update_cmd = 'helm dep up {}'.format(source_path.as_posix())
    helm_template_cmd = 'helm template {} {} --namespace {} --values {} --debug > {}'.format(app_name,
                                                                                             source_path.as_posix(),
                                                                                             args.n,
                                                                                             env_path.as_posix(),
                                                                                             temp_all_in_one_path.as_posix())

    cmd.append(helm_dep_update_cmd)
    cmd.append(helm_template_cmd)
    execute_shell(cmd_func("&&".join(cmd)))
    with io.open(temp_all_in_one_path, "r", encoding="utf-8", newline="\n") as o_file:
        y = yaml.load_all(o_file.read(), Loader=yaml.UnsafeLoader)
    with io.open(temp_all_in_one_path, "w+", encoding="utf-8", newline="\n") as y_file:
        all_doc=[]
        for content in y:
            if content and content["metadata"] and "namespace" not in content["metadata"].keys():
                content["metadata"]["namespace"] = args.n
            all_doc.append(content)
        yaml.dump_all(all_doc, y_file, Dumper=yaml.RoundTripDumper,default_flow_style=False, explicit_start=True)
    execute_shell(kube_cmd)

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
    parser.add_argument('-d', action="store_true")
    parser.add_argument("-t", default=2)
    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    parser.add_argument('-n', default=selected_option["namespace"])
    args = parser.parse_args()
    execute(selected_option["list"], apply, env_path=env_path, args=args)
