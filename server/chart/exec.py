#!/usr/bin/env python3
import argparse
import yaml
import jinja2
import share

from pathlib import Path


def invoke(role_title: str, role_path: Path, **kwargs):
    args = kwargs["args"]
    env_dict: dict = kwargs["env_dict"]

    role_name = role_path.name
    role_values_file = role_path.joinpath("values.yaml")

    temp_all_in_one_path = role_path.joinpath("___temp/deploy.yaml")
    temp_all_in_one_path.parent.mkdir(parents=True, exist_ok=True)
    temp_all_in_one_path.touch()

    if role_values_file.exists():
        with open(role_values_file, "r", encoding="utf-8", newline="\n") as r_file:
            content = jinja2.Template(r_file.read()).render(**env_dict)
            with open(role_values_file, "w", encoding="utf-8") as t_file:
                t_file.write(content)

    def helm_action_cmd():
        _action = args.a
        _extension = ""
        if _action == "delete":
            return "helm delete {0} {1}".format(role_name, "" if args.skip_namespace else "--namespace {0}".format(args.n))
        if _action == "install":
            _action = "upgrade --install"
        helm_cmd = [
            "helm {0} {1} {2}".format(_action, role_name, role_path.as_posix()),
            "--set {0}".format(",".join(["=".join([k, "\"" + v + "\""]) for (k, v) in env_dict.items()]))
        ]
        if not args.ignore_namespace:
            helm_cmd.append("--namespace {0}".format(args.n))
        if args.create_namespace:
            helm_cmd.append("--create-namespace")
        if _action == "template":
            helm_cmd.append("> {0}".format(temp_all_in_one_path))
        return "&&".join([
            'helm dep up {0}'.format(role_path.as_posix()),
            share.arr_param_to_str(helm_cmd)
        ])

    _cmds = [
        share.role_print(role_title, args.a, temp_all_in_one_path.as_posix())
    ]

    if args.a == "push":
        helm_repo_name = env_dict["param_helm_repo_name"]
        helm_repo_url = env_dict["param_helm_repo_url"]
        helm_username = env_dict["param_helm_username"]
        helm_password = env_dict["param_helm_password"]
        _cmds.append(share.arr_param_to_str([
            "helm plugin list | if [ -z \"$(grep -w nexus-push)\" ];then helm plugin install --version master https://github.com/sonatype-nexus-community/helm-nexus-push.git;fi",
            "helm repo   list | if [ -z \"$(grep -w {0})\" ];then helm repo add {0} {1};fi".format(helm_repo_name, helm_repo_url),
            "helm package {0} --destination {0} | sed 's/Successfully packaged chart and saved it to: //g' | xargs helm nexus-push {1}  --username {2} --password {3}".format(role_path, helm_repo_name, helm_username, helm_password)
        ], separator=" && "))
    else:
        _cmds.append(helm_action_cmd())
    _cmd_str = share.arr_param_to_str(_cmds, separator=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    yaml.add_representer(str, lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, '|' if '\n' in data else ''))
    env_file = Path(__file__).parent.joinpath(".env")
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs="+", default=[])
    parser.add_argument('-a', type=str, required=True)
    parser.add_argument("-t", default=2)
    parser.add_argument('-n')
    parser.add_argument('--ignore-namespace', action="store_true")
    parser.add_argument('--create-namespace', action="store_true")
    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    share.execute(selected_option["list"], invoke, env_file=env_file, args=args)
