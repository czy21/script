#!/usr/bin/env python3
import argparse
import pathlib

import share
import yaml

from utility import collection as collection_util, file as file_util


def invoke(role_title: str, role_path: pathlib.Path, role_env: dict, args: argparse.Namespace, **kwargs):
    role_name = role_path.name
    role_values_override_file = role_path.joinpath("values.override.yaml")

    temp_all_in_one_path = role_path.joinpath("___temp/deploy.yaml")
    temp_all_in_one_path.parent.mkdir(parents=True, exist_ok=True)
    temp_all_in_one_path.touch()

    file_util.write_file(role_values_override_file, lambda f: yaml.dump(role_env, f))

    _cmds = []

    if args.action == "push":
        helm_repo_name = role_env.get("param_helm_repo_name")
        helm_repo_url = role_env.get("param_helm_repo_url")
        helm_username = role_env.get("param_helm_username")
        helm_password = role_env.get("param_helm_password")
        _cmds.append(share.echo_action(role_title, "push"))
        _cmds.append("helm plugin list | if [ -z \"$(grep -w nexus-push)\" ];then helm plugin install --version master https://github.com/sonatype-nexus-community/helm-nexus-push.git;fi")
        _cmds.append("helm repo   list | if [ -z \"$(grep -w {0})\" ];then helm repo add {0} {1};fi".format(helm_repo_name, helm_repo_url))
        _cmds.append("helm package {0} --destination {0} | sed 's/Successfully packaged chart and saved it to: //g' | xargs helm nexus-push {1}  --username {2} --password {3}".format(role_path, helm_repo_name, helm_username, helm_password))

    else:
        _action = args.action
        _extension = ""
        if args.delete:
            _cmds.append([
                share.echo_action(role_title, "delete"),
                "helm delete {0} {1}".format(role_name, "" if args.ignore_namespace else "--namespace {0}".format(args.namespace))
            ])
        else:
            if args.install:
                _cmds.append(share.echo_action(role_title, "install"))
                _action = "upgrade --install"
            helm_cmd = [
                "helm {0} {1} {2} --values {3}".format(_action, role_name, role_path.as_posix(), role_values_override_file)
            ]
            if not args.ignore_namespace:
                helm_cmd.append("--namespace {0}".format(args.namespace))
            if args.create_namespace:
                helm_cmd.append("--create-namespace")
            if _action == "template":
                _cmds.append(share.echo_action(role_title, "template"))
                helm_cmd.append("> {0}".format(temp_all_in_one_path))

            _cmds.append('helm dep up {0}'.format(role_path.as_posix()))
            _cmds.append(collection_util.flat_to_str(helm_cmd))
    _cmd_str = collection_util.flat_to_str(_cmds, delimiter=" && ")
    share.run_cmd(_cmd_str)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke, role_deep=2)
    installer.arg_parser.add_argument('--ignore-namespace', action="store_true")
    installer.arg_parser.add_argument('--create-namespace', action="store_true")
    installer.run()
