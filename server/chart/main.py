#!/usr/bin/env python3
import pathlib

import yaml

from server import share
from utility import (
    collection as collection_util,
    file as file_util,
    template as template_util
)


class ChartRole(share.AbstractRole):

    def __init__(self,
                 home_path: pathlib.Path = None,
                 root_path: pathlib.Path = None,
                 namespace: str = None,
                 role_title: str = None,
                 role_name: str = None,
                 role_path: pathlib.Path = None,
                 role_output_path: pathlib.Path = None,
                 role_env: dict = None,
                 role_env_output_file: pathlib.Path = None,
                 args=None) -> None:
        super().__init__(home_path, root_path, namespace, role_title, role_name, role_path, role_output_path, role_env, role_env_output_file, args)
        self.root_doc_template_file = root_path.joinpath("doc-template.md")
        self.role_values_override_file = role_output_path.joinpath("values.override.yaml")
        file_util.write_text(self.role_values_override_file, yaml.dump(role_env))

    def install(self) -> list[str]:
        _cmds = ['helm dep up {0}'.format(self.role_output_path.as_posix())]
        cmd = [
            "helm {0} {1} {2} --values {3}".format("upgrade --install", self.role_name, self.role_output_path.as_posix(), self.role_values_override_file)
        ]
        if not self.args.ignore_namespace:
            cmd.append("--namespace {0}".format(self.namespace))
        if self.args.create_namespace:
            cmd.append("--create-namespace")
        _cmds.append(collection_util.flat_to_str(cmd))
        return _cmds

    def build(self) -> list[str]:
        _cmds = []
        if self.args.target == "doc":
            if self.any_doc_exclude(self.role_output_path):
                md_content = template_util.Template(file_util.read_text(self.root_doc_template_file)).render(**{
                    "param_registry_git_repo_dict": {t["name"]: "{}/{}/{}".format(t["url"], "tree/main", self.role_name) for t in self.role_env.get("param_registry_git_repos")}
                })
                role_readme = self.role_output_path.joinpath("README.md")
                file_util.write_text(self.role_output_path.joinpath("doc.md"), md_content + "\n" + (file_util.read_text(role_readme) if role_readme.exists() else ""))
            self.sync_to_git_repo("chart")
        return _cmds

    def delete(self) -> list[str]:
        return ["helm delete {0} {1}".format(self.role_name, "" if self.args.ignore_namespace else "--namespace {0}".format(self.namespace))]

    def backup(self) -> list[str]:
        return []

    def restore(self) -> list[str]:
        return []

    def push(self) -> list[str]:
        _cmds = []
        helm_repo_name = self.role_env.get("param_helm_repo_name")
        helm_repo_url = self.role_env.get("param_helm_repo_url")
        helm_username = self.role_env.get("param_helm_username")
        helm_password = self.role_env.get("param_helm_password")
        _cmds.append("helm plugin list | if [ -z \"$(grep -w nexus-push)\" ];then helm plugin install --version master https://github.com/sonatype-nexus-community/helm-nexus-push.git;fi")
        _cmds.append("helm repo   list | if [ -z \"$(grep -w {0})\" ];then helm repo add {0} {1};fi".format(helm_repo_name, helm_repo_url))
        _cmds.append(
            "helm package {0} --destination {0} | sed 's/Successfully packaged chart and saved it to: //g' | xargs helm nexus-push {1}  --username {2} --password {3}".format(
                self.role_output_path, helm_repo_name,
                helm_username,
                helm_password
            )
        )
        return _cmds


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, ChartRole, role_deep=2).run()
