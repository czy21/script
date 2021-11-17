#!/usr/bin/env python3
import argparse
import io
import share
from pathlib import Path
from ruamel import yaml


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
    kube_cmd = get_kube_cmd(kubectl_action, temp_all_in_one_path.as_posix())
    cmd_func = lambda x: 'bash -xc \'{}\''.format(x)

    pre_cmd = share.arr_param_to_str(
        [
            share.role_print(app_id, "deploy", temp_all_in_one_path.as_posix()),
            'helm dep up {}'.format(source_path.as_posix()),
            'helm template {} {} --namespace {} --values {} --debug > {}'.format(app_name,
                                                                                 source_path.as_posix(),
                                                                                 args.n,
                                                                                 env_path.as_posix(),
                                                                                 temp_all_in_one_path.as_posix())
        ], separator=" && ")
    share.execute_cmd(pre_cmd)
    with io.open(temp_all_in_one_path, "r", encoding="utf-8", newline="\n") as o_file:
        y = yaml.load_all(o_file.read(), Loader=yaml.UnsafeLoader)
    with io.open(temp_all_in_one_path, "w+", encoding="utf-8", newline="\n") as y_file:
        all_doc = []
        for content in y:
            if content and content["metadata"] and "namespace" not in content["metadata"].keys():
                content["metadata"]["namespace"] = args.n
            all_doc.append(content)
        yaml.dump_all(all_doc, y_file, Dumper=yaml.RoundTripDumper, default_flow_style=False, explicit_start=True)
    share.execute_cmd(kube_cmd)


if __name__ == '__main__':
    env_path = Path(__file__).parent.joinpath("env.yaml")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action="store_true")
    parser.add_argument("-t", default=2)
    parser.add_argument('-n')
    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    execute(selected_option["list"], apply, env_path=env_path, args=args)
