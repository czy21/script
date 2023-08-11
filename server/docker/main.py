#!/usr/bin/env python3

import argparse
import logging
import pathlib

import share
# from script.server import share
import urllib3.util
from utility import (
    collection as collection_util,
    path as path_util,
    file as file_util,
    regex as regex_util
)

logger = logging.getLogger()


class DockerRole(share.AbstractRole):

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
                 args: argparse.Namespace = None) -> None:
        super().__init__(home_path, root_path, namespace, role_title, role_name, role_path, role_output_path, role_env, role_env_output_file, args)
        self.root_deploy_file = root_path.joinpath("deploy.yml")
        self.role_deploy_file = role_output_path.joinpath("deploy.yml")
        self.role_conf_path = role_output_path.joinpath("conf")
        self.role_init_sh = role_output_path.joinpath("init.sh")
        self.role_node_name = self.role_env.get("param_cluster_name")
        self.target_app_path = pathlib.Path(self.role_env.get("param_docker_data")).joinpath(self.role_name)
        self.param_role_target_path = self.role_env.get("param_role_target_path")
        if self.param_role_target_path:
            self.target_app_path = pathlib.Path(self.param_role_target_path)
        self.role_node_path = self.role_output_path.joinpath("node")
        self.role_node_target_path = next(filter(lambda a: a.is_dir and str(a.name) == self.role_node_name, self.role_node_path.glob("*")), None) if self.role_node_path.exists() else None
        self.role_node_target_deploy_file = None
        self.role_node_target_conf_path = None
        if self.role_node_target_path:
            path_util.merge_dir(self.role_output_path, self.role_node_target_path, ["node", "deploy.yml"])
            self.role_node_target_conf_path = self.role_node_target_path.joinpath("conf")
            self.role_node_target_deploy_file = self.role_node_target_path.joinpath("deploy.yml")

    def docker_compose_cmd(self, option):
        role_deploy_files = [
            self.root_deploy_file,
            self.role_deploy_file.as_posix()
        ]
        if self.role_node_target_deploy_file and self.role_node_target_deploy_file.exists():
            role_deploy_files.append(self.role_node_target_deploy_file)
        role_project_name = self.role_env.get("param_role_project_name")
        return 'sudo docker-compose --project-name {0} {1} {2}'.format(
            role_project_name if role_project_name else self.role_name,
            " ".join(["--file {0}".format(t) for t in role_deploy_files]), option)

    def install(self) -> list[str]:
        _cmds = []
        if self.role_conf_path.exists() or (self.role_node_target_conf_path and self.role_node_target_conf_path.exists()):
            if self.args.rm_conf:
                target_role_conf_path = self.target_app_path.joinpath("conf")
                if target_role_conf_path.exists() and self.target_app_path.name == self.role_name:
                    role_conf_relative_files = set(file_util.get_files(self.role_conf_path, self.role_output_path.as_posix()))
                    remove_conf_files = [
                        t.as_posix()
                        for t in filter(lambda a: a.is_file(), target_role_conf_path.rglob("*"))
                        if not any([t.as_posix().__contains__(s) for s in role_conf_relative_files])
                    ]
                    if remove_conf_files:
                        _cmds.append(share.echo_action(self.role_title, "remove conf"))
                        _cmds.append("sudo rm -rfv {0}".format(" ".join(remove_conf_files)))
            _cmds.append('sudo mkdir -p {1} && sudo cp -rv {0} {1}'.format(
                self.role_node_target_conf_path if self.role_node_target_conf_path and self.role_node_target_conf_path.exists() else self.role_conf_path.as_posix(),
                self.target_app_path.as_posix())
            )
        if self.role_init_sh.exists():
            _cmds.append("bash {}".format(self.role_init_sh.as_posix()))
        if self.role_deploy_file.exists():
            if self.args.debug:
                _cmds.append(self.docker_compose_cmd("config"))
            up_args = ["up --detach --build --remove-orphans"]
            if self.args.recreate:
                up_args.append("--force-recreate")
            _cmds.append(self.docker_compose_cmd(collection_util.flat_to_str(up_args)))
        return _cmds

    def build(self) -> list[str]:
        _cmds = []
        if self.args.target.startswith("Dockerfile"):
            role_dockerfile = self.role_output_path.joinpath(self.args.target)
            registry_source_url = self.role_env['param_registry_url']
            registry_source_dir = self.role_env['param_registry_dir']
            registry_source_url = path_util.join_path(registry_source_url, registry_source_dir)
            if role_dockerfile.exists():
                registry_source_tag = path_util.join_path(registry_source_url, self.role_name)
                if self.args.tag:
                    registry_source_tag = registry_source_tag + ":" + self.args.tag
                registry_targets = self.args.param.get("param_registry_targets").split(",") if self.args.param.get("param_registry_targets") else []
                registry_target_tags = []
                for t in registry_targets:
                    registry_target_url = self.role_env.get("param_registry_{0}_url".format(t))
                    registry_target_dir = self.role_env.get("param_registry_{0}_dir".format(t))
                    if not registry_target_url:
                        logger.warning("registry_target: {} not exist".format(t))
                        continue
                    target_registry_tag = path_util.join_path(registry_target_url, registry_target_dir, self.role_name)
                    if self.args.tag:
                        target_registry_tag = target_registry_tag + ":" + self.args.tag
                    registry_target_tags.append(target_registry_tag)
                _cmds.append("docker build --tag {0} --file {1} {2} --pull".format(registry_source_tag, role_dockerfile.as_posix(), self.role_output_path.as_posix()))
                _cmds.extend(["docker tag {} {}".format(registry_source_tag, t) for t in registry_target_tags])
                if self.args.push:
                    _cmds.append("docker push {0}".format(registry_source_tag))
                    _cmds.extend(["docker push {0}".format(t) for t in registry_target_tags])
                if registry_targets:
                    registry_git_repo: str = self.role_env["param_registry_git_repo"]
                    registry_git_repo_url: urllib3.util.Url = urllib3.util.parse_url(registry_git_repo)
                    registry_git_repo_name: str = pathlib.Path(registry_git_repo_url.path).name
                    registry_git_repo_dir: pathlib.Path = self.home_path.joinpath(registry_git_repo_name)
                    if not registry_git_repo_dir.exists():
                        share.execute("git clone {0} {1}".format(registry_git_repo.replace("https://github.com", "git@github.com:"), registry_git_repo_dir))
                    registry_github_repo_role_dir = registry_git_repo_dir.joinpath(self.role_name)
                    registry_github_repo_role_dir.mkdir(exist_ok=True)
                    sync_is_change = file_util.sync(self.role_output_path,
                                                    lambda a: any(regex_util.match_rules(["Dockerfile*", "docker-entrypoint.sh"], a.as_posix()).values()),
                                                    registry_github_repo_role_dir)
                    if sync_is_change:
                        _cmds.append("cd {0} && git add . && git commit -m \"# add or update {1} Dockerfile\" && git push && cd".format(registry_github_repo_role_dir.as_posix(), self.role_name))
        return _cmds

    def delete(self) -> list[str]:
        _cmds = []
        if self.role_deploy_file.exists():
            _cmds.append(self.docker_compose_cmd("down --remove-orphans"))
        return _cmds

    def backup(self) -> list[str]:
        return []

    def restore(self) -> list[str]:
        return []

    def push(self) -> list[str]:
        return []


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, DockerRole, role_deep=2).run()
