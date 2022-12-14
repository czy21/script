#!/usr/bin/env python3
import argparse
import pathlib

import share
import yaml

from utility import (
    collection as collection_util,
    file as file_util
)


def invoke(role_title: str,
           role_name: str,
           role_path: pathlib.Path,
           role_output_path: pathlib.Path,
           role_env: dict,
           namespace: str,
           args: argparse.Namespace,
           **kwargs):
    role_values_override_file = role_output_path.joinpath("values.override.yaml")

    file_util.write_text(role_values_override_file, yaml.dump(role_env))

    _cmds = []

    if args.command == "push":
        helm_repo_name = role_env.get("param_helm_repo_name")
        helm_repo_url = role_env.get("param_helm_repo_url")
        helm_username = role_env.get("param_helm_username")
        helm_password = role_env.get("param_helm_password")
        _cmds.append(share.echo_action(role_title, "push"))
        _cmds.append("helm plugin list | if [ -z \"$(grep -w nexus-push)\" ];then helm plugin install --version master https://github.com/sonatype-nexus-community/helm-nexus-push.git;fi")
        _cmds.append("helm repo   list | if [ -z \"$(grep -w {0})\" ];then helm repo add {0} {1};fi".format(helm_repo_name, helm_repo_url))
        _cmds.append(
            "helm package {0} --destination {0} | sed 's/Successfully packaged chart and saved it to: //g' | xargs helm nexus-push {1}  --username {2} --password {3}".format(
                role_output_path, helm_repo_name,
                helm_username,
                helm_password
            )
        )

    else:
        _command = args.command
        _extension = ""
        if args.command == "delete":
            _cmds.append([
                share.echo_action(role_title, "delete"),
                "helm delete {0} {1}".format(role_name, "" if args.ignore_namespace else "--namespace {0}".format(namespace))
            ])
        else:
            if args.command == "install":
                _cmds.append(share.echo_action(role_title, "install"))
                _command = "upgrade --install"
            helm_cmd = [
                "helm {0} {1} {2} --values {3}".format(_command, role_name, role_output_path.as_posix(), role_values_override_file)
            ]
            if not args.ignore_namespace:
                helm_cmd.append("--namespace {0}".format(namespace))
            if args.create_namespace:
                helm_cmd.append("--create-namespace")

            _cmds.append('helm dep up {0}'.format(role_output_path.as_posix()))
            _cmds.append(collection_util.flat_to_str(helm_cmd))
    _cmd_str = collection_util.flat_to_str(_cmds, delimiter=" && ")
    share.execute(_cmd_str, dry_run=args.dry_run)


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, invoke, role_deep=2)
    installer.run()
