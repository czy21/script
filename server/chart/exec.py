#!/usr/bin/env python3
import argparse
import pathlib

import jinja2
import share
import yaml


def invoke(role_title: str, role_path: pathlib.Path, **kwargs):
    args = kwargs["args"]
    env_dict: dict = kwargs["env_dict"]

    role_name = role_path.name
    role_values_override_file = role_path.joinpath("values.override.yaml")

    temp_all_in_one_path = role_path.joinpath("___temp/deploy.yaml")
    temp_all_in_one_path.parent.mkdir(parents=True, exist_ok=True)
    temp_all_in_one_path.touch()

    with open(role_values_override_file, "w", encoding="utf-8") as ovf:
        yaml.dump(env_dict, ovf)

    _cmds = [
        share.role_print(role_title, args.a)
    ]

    if args.a == "push":
        helm_repo_name = env_dict["param_helm_repo_name"]
        helm_repo_url = env_dict["param_helm_repo_url"]
        helm_username = env_dict["param_helm_username"]
        helm_password = env_dict["param_helm_password"]
        _cmds.append("helm plugin list | if [ -z \"$(grep -w nexus-push)\" ];then helm plugin install --version master https://github.com/sonatype-nexus-community/helm-nexus-push.git;fi")
        _cmds.append("helm repo   list | if [ -z \"$(grep -w {0})\" ];then helm repo add {0} {1};fi".format(helm_repo_name, helm_repo_url))
        _cmds.append("helm package {0} --destination {0} | sed 's/Successfully packaged chart and saved it to: //g' | xargs helm nexus-push {1}  --username {2} --password {3}".format(role_path, helm_repo_name, helm_username, helm_password))

    else:
        _action = args.a
        _extension = ""
        if _action == "delete":
            return "helm delete {0} {1}".format(role_name, "" if args.ignore_namespace else "--namespace {0}".format(args.n))
        if _action == "install":
            _action = "upgrade --install"
        helm_cmd = [
            "helm {0} {1} {2} --values {3}".format(_action, role_name, role_path.as_posix(), role_values_override_file)
        ]
        if not args.ignore_namespace:
            helm_cmd.append("--namespace {0}".format(args.n))
        if args.create_namespace:
            helm_cmd.append("--create-namespace")
        if _action == "template":
            helm_cmd.append("> {0}".format(temp_all_in_one_path))
        _cmds.append('helm dep up {0}'.format(role_path.as_posix()))
        _cmds.append(share.flat_to_str(helm_cmd))
    _cmd_str = share.flat_to_str(_cmds, delimiter=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    env_file = root_path.joinpath("env.yaml")
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", default=[])
    parser.add_argument('-a', type=str, required=True)
    parser.add_argument('-n')
    parser.add_argument('--ignore-namespace', action="store_true")
    parser.add_argument('--create-namespace', action="store_true")
    args = parser.parse_args()
    selected_option = share.select_option(2)
    if args.n is None:
        args.n = selected_option["namespace"]
    share.execute(selected_option, invoke, root_path=root_path.as_posix(), env_file=env_file, args=args)
