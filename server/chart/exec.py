#!/usr/bin/env python3
import argparse
import io
import yaml
import jinja2
import share

from pathlib import Path


def get_kube_cmd(action: str, yaml_path: str):
    return 'kubectl {0} --filename={1} '.format(action, yaml_path)


def invoke(role_title: str, role_path: Path, **kwargs):
    args = kwargs["args"]
    ctl = args.ctl
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
        if ctl == "helm" and _action == "delete":
            return "helm delete {0} --namespace {1}".format(role_name, args.n)
        if ctl == "helm" and _action == "install":
            _action = "upgrade --install"
        if ctl == "kubectl":
            _action = "template"
            _extension = "> {0}".format(temp_all_in_one_path)
        return "&&".join([
            'helm dep up {0}'.format(role_path.as_posix()),
            'helm {0} {1} {2} --namespace {3} --set {4} {5}'.format(_action,
                                                                    role_name,
                                                                    role_path.as_posix(),
                                                                    args.n,
                                                                    ",".join(["=".join([k, "\"" + v + "\""]) for (k, v) in env_dict.items()]),
                                                                    _extension)])

    cmds = [
        share.role_print(role_title, "deploy", temp_all_in_one_path.as_posix())
    ]
    if ctl == "helm":
        if args.a == "push":
            helm_repo_name = env_dict["param_helm_repo_name"]
            helm_repo_url = env_dict["param_helm_repo_url"]
            helm_username = env_dict["param_helm_username"]
            helm_password = env_dict["param_helm_password"]
            cmds.append(share.arr_param_to_str(
                [
                    "helm plugin list | if [ -z \"$(grep nexus-push)\" ];then helm plugin install --version master https://github.com/sonatype-nexus-community/helm-nexus-push.git;fi",
                    "helm repo   list | if [ -z \"$(grep {0})\" ];then helm repo add {0} {1};fi".format(helm_repo_name, helm_repo_url),
                    "helm package {0} --destination {0} | sed 's/Successfully packaged chart and saved it to: //g' | xargs helm nexus-push {1}  --username {2} --password {3}".format(role_path, helm_repo_name, helm_username, helm_password)
                ], separator=" && "))
        else:
            cmds.append(helm_action_cmd())
    elif ctl == "kubectl":
        with io.open(temp_all_in_one_path, "r", encoding="utf-8", newline="\n") as o_file:
            y = yaml.unsafe_load_all(o_file.read())
        with io.open(temp_all_in_one_path, "w+", encoding="utf-8", newline="\n") as y_file:
            all_doc = []
            for content in y:
                if content:
                    if content["metadata"] and "namespace" not in content["metadata"].keys():
                        content["metadata"]["namespace"] = args.n
                    all_doc.append(content)
            yaml.dump_all(all_doc, y_file)
        cmds.append(helm_action_cmd())
        cmds.append(get_kube_cmd(args.a, temp_all_in_one_path.as_posix()))
    _cmd_str = share.arr_param_to_str(cmds, separator=" && ")
    share.execute_cmd(_cmd_str)


if __name__ == '__main__':
    yaml.add_representer(str, lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, '|' if '\n' in data else ''))
    env_file = Path(__file__).parent.joinpath(".env")
    parser = argparse.ArgumentParser()
    parser.add_argument('--ctl', default="kubectl")
    parser.add_argument('-p', nargs="+", default=[])
    parser.add_argument('-a', type=str, required=True)
    parser.add_argument("-t", default=2)
    parser.add_argument('-n')
    args = parser.parse_args()
    selected_option = share.select_option(int(args.t))
    if args.n is None:
        args.n = selected_option["namespace"]
    share.execute(selected_option["list"], invoke, env_file=env_file, args=args)
