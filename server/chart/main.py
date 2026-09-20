#!/usr/bin/env python3

import logging

import json
import pathlib
import re
import requests

import server
from util import (
    basic as basic_util,
    collection as collection_util,
    file as file_util,
    template as template_util,
    yaml as yaml_util,
)

logger = logging.getLogger()


class ChartRole(server.AbstractRole):

    def __init__(self, context: server.RoleContext) -> None:
        super().__init__(context)

        self.role_init_sh = context.role_out_path.joinpath("init.sh")
        self.role_chart_file = self.context.role_path / "Chart.yaml"
        self.role_values_override_file = context.role_out_path.joinpath("values.override.yaml")
        file_util.write_text(self.role_values_override_file, yaml_util.dump(context.role_env))

    def install(self) -> list[str]:
        _cmds = []
        if self.role_init_sh.exists():
            _cmds.append("bash {}".format(self.role_init_sh.as_posix()))
        _cmds.append(f'helm dep up {self.context.role_out_path.as_posix()}')
        cmd = [
            f"helm upgrade --install {self.context.role_name} {self.context.role_out_path.as_posix()} --values {self.role_values_override_file}"
        ]
        if not self.context.args.ignore_namespace:
            cmd.append("--namespace {0}".format(self.context.namespace))
        if self.context.args.create_namespace:
            cmd.append("--create-namespace")
        if self.context.args.dry_run:
            cmd.append("--dry-run")
        cmd = collection_util.flat_to_str(cmd)
        _cmds.append(cmd)
        return _cmds

    def build(self) -> list[str]:
        _cmds = []
        helm_repo_url = self.context.role_env.get("param_helm_repo_url")
        if self.context.args.target == "Chart":
            if self.context.args.push:
                _cmds.append(f"helm package {self.context.role_out_path} --destination {self.context.role_out_path} | sed 's/Successfully\\(.*\\)to: //g' | xargs -I{{}} helm push {{}} {helm_repo_url}")
            else:
                _cmds.append(f"helm package {self.context.role_out_path} --destination {self.context.role_out_path}")
        repositories = []
        if self.context.args.target == "doc" or self.context.args.check:
            _check_cmds = []
            images = self.context.role_build_path / 'images'
            charts = self.context.role_build_path / 'charts'
            _check_cmds.append(f"helm dependency list {self.context.role_out_path} 2>/dev/null | sed '/^$/d;1d' | awk '{{if ($3 ~ /^oci:\\/\\//) print substr($3, 7) \"/\" $1 \":\" $2 >> \"{images.as_posix()}\"; else print $3 \" \" $1 \" \" $2 >> \"{charts.as_posix()}\"}}'")
            server.execute(collection_util.flat_to_str(_check_cmds, delimiter=" && "))
            repositories.extend(super().get_check_images(images))
            repositories.extend(self.get_check_charts(charts))
        if self.context.args.target == "doc":
            registry_git_repo_raw_format = self.context.role_env.get("param_registry_git_repo_raw") + "/main/{0}/chart/{1}"
            self.role_doc_content = template_util.Template(file_util.read_text(self.root_doc_template_file)).render(**{
                "param_role_name": self.context.role_name,
                "param_registry_git_repo": "{}/{}/{}".format(self.context.role_env.get("param_registry_git_repo"), "tree/main", self.context.role_name),
                "param_repositories": repositories,
                "param_role_install": {
                    "name": self.role_chart_file.name,
                    "command": f'helm dep up && helm upgrade --install {self.context.role_name}',
                    "rawUrl": registry_git_repo_raw_format.format(self.context.role_name, self.role_chart_file.name)
                } if self.role_chart_file.exists() else None
            })
        return _cmds

    def get_check_charts(self, charts_file):
        token_cache = {}
        repositories = []
        if not charts_file.exists():
            return repositories

        def get_repository_cache(repository_index):
            if repository_index in token_cache:
                return token_cache[repository_index]
            response = requests.get(repository_index)
            response.raise_for_status()
            response.encoding = "utf-8"
            token_cache[repository_index] = yaml_util.load(response.text)
            return token_cache.get(repository_index)

        for l in file_util.read_text(charts_file).splitlines():
            repository, name, version = l.split(' ')
            version_major_match = re.match(r'v?(\d+)', version)
            version_major = int(version_major_match.group(1)) if version_major_match else None

            try:
                repository_obj = {
                    'repository': repository,
                    'name': name,
                    'version': version
                }

                repository_index = f"{repository.rstrip('/')}/index.yaml"
                repository_index = get_repository_cache(repository_index)
                repository_list = sorted([x for x in repository_index.get('entries', {}).get(name, [])], key=lambda x: basic_util.get_version_number(x.get('version')), reverse=True)
                repository_tags = [x.get('version') for x in repository_list]
                repository_obj['latest'] = max((x for x in repository_tags if (v := basic_util.get_version_number(x)) and v[0] == version_major), key=basic_util.get_version_number, default=None) or version
                repository_obj['releases'] = repository_tags[:5]

                repositories.append(repository_obj)
                logger.debug(json.dumps(repository_obj))
            except Exception as e:
                logger.error(f"{self.context.role_path}: {e}")
        return repositories

    def delete(self) -> list[str]:
        return ["helm delete {0} {1}".format(self.context.role_name, "" if self.context.args.ignore_namespace else "--namespace {0}".format(self.context.namespace))]

    def backup(self) -> list[str]:
        return []

    def restore(self) -> list[str]:
        return []


if __name__ == '__main__':
    server.Installer(pathlib.Path(__file__).parent, role_impl=ChartRole, role_deep=2).run()
