#!/usr/bin/env python3
import argparse
import io
from pathlib import Path

import share
import yaml


def execute(app_tuples, func, **kwargs):
    yaml.add_representer(str, lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, '|' if '\n' in data else ''))
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

    with io.open(env_path, "r", encoding="utf-8", newline="\n") as ef:
        env_dict = yaml.unsafe_load(ef.read())
    kube_actions = ["apply", "delete"]
    temp_all_in_one_path = source_path.joinpath("___temp/deploy.yaml")
    temp_all_in_one_path.parent.mkdir(parents=True, exist_ok=True)
    temp_all_in_one_path.touch()
    if list(filter(lambda f: f in kube_actions, args.a)):
        pre_cmd = share.arr_param_to_str(
            [
                share.role_print(app_id, "deploy", temp_all_in_one_path.as_posix()),
                'helm dep up {0}'.format(source_path.as_posix()),
                'helm template {0} {1} --namespace {2} --values {3} --debug > {4}'.format(app_name,
                                                                                          source_path.as_posix(),
                                                                                          args.n,
                                                                                          env_path.as_posix(),
                                                                                          temp_all_in_one_path.as_posix())
            ], separator=" && ")
        share.execute_cmd(pre_cmd)
        with io.open(temp_all_in_one_path, "r", encoding="utf-8", newline="\n") as o_file:
            y = yaml.unsafe_load_all(o_file.read())
        with io.open(temp_all_in_one_path, "w+", encoding="utf-8", newline="\n") as y_file:
            all_doc = []
            for content in y:
                if content and content["metadata"] and "namespace" not in content["metadata"].keys():
                    content["metadata"]["namespace"] = args.n
                all_doc.append(content)
            yaml.dump_all(all_doc, y_file)
    for action in args.a:
        if action == "push":
            helm_registry = env_dict["helm"]["registry"]
            helm_username = env_dict["helm"]["username"]
            helm_password = env_dict["helm"]["password"]
            helm_push_cmd = share.arr_param_to_str(
                [
                    "helm plugin list | if [ -z \"$(grep nexus-push)\" ];then helm plugin install --version master https://github.com/sonatype-nexus-community/helm-nexus-push.git;fi",
                    "helm package {0} --destination {0} | sed 's/Successfully packaged chart and saved it to: //g' | xargs helm nexus-push {1}  --username {2} --password {3}".format(source_path, helm_registry, helm_username, helm_password)
                ], separator=" && ")
            share.execute_cmd(helm_push_cmd)
        if action in kube_actions:
            kube_cmd = get_kube_cmd(action, temp_all_in_one_path.as_posix())
            share.execute_cmd(kube_cmd)


if __name__ == '__main__':
    env_path = Path(__file__).parent.joinpath("env.yaml")
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs="+", required=True)
    parser.add_argument("-t", default=2)
    parser.add_argument('-n')
    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    execute(selected_option["list"], apply, env_path=env_path, args=args)
