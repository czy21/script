#!/usr/bin/env python3

import argparse
import logging
import pathlib

import share
import urllib3.util
from utility import (
    collection as collection_util,
    path as path_util,
    file as file_util,
    regex as regex_util
)

logger = logging.getLogger()


def get_cmds(home_path: pathlib.Path,
             role_title: str,
             role_name: str,
             role_path: pathlib.Path,
             role_output_path: pathlib.Path,
             role_env: dict,
             namespace: str,
             args: argparse.Namespace,
             **kwargs):
    role_node_name = role_env.get("param_cluster_name")
    role_conf_path = role_output_path.joinpath("conf")
    role_deploy_file = role_output_path.joinpath("deploy.yml")
    role_init_sh = role_output_path.joinpath("init.sh")

    target_app_path = pathlib.Path(role_env.get("param_docker_data")).joinpath(role_name)
    param_role_target_path = role_env.get("param_role_target_path")
    if param_role_target_path:
        target_app_path = pathlib.Path(param_role_target_path)
    role_node_path = role_output_path.joinpath("node")
    role_node_target_path = next(filter(lambda a: a.is_dir and str(a.name) == role_node_name, role_node_path.glob("*")), None) if role_node_path.exists() else None
    role_node_target_deploy_file = None
    role_node_target_conf_path = None
    if role_node_target_path:
        path_util.merge_dir(role_output_path, role_node_target_path, ["node", "deploy.yml"])
        role_node_target_conf_path = role_node_target_path.joinpath("conf")
        role_node_target_deploy_file = role_node_target_path.joinpath("deploy.yml")
    _cmds = []

    def docker_compose_cmd(option):
        role_deploy_files = [
            kwargs.get("base_deploy_file"),
            role_deploy_file.as_posix()
        ]
        if role_node_target_deploy_file and role_node_target_deploy_file.exists():
            role_deploy_files.append(role_node_target_deploy_file)
        role_project_name = role_env.get("param_role_project_name")
        return 'sudo docker-compose --project-name {0} {1} {2}'.format(
            role_project_name if role_project_name else role_name,
            " ".join(["--file {0}".format(t) for t in role_deploy_files]), option)

    if args.command == share.Command.install.value:
        if role_conf_path.exists() or (role_node_target_conf_path and role_node_target_conf_path.exists()):
            if args.rm_conf:
                target_role_conf_path = target_app_path.joinpath("conf")
                if target_role_conf_path.exists() and target_app_path.name == role_name:
                    role_conf_relative_files = set(file_util.get_files(role_conf_path, role_output_path.as_posix()))
                    remove_conf_files = [
                        t.as_posix()
                        for t in filter(lambda a: a.is_file(), target_role_conf_path.rglob("*"))
                        if not any([t.as_posix().__contains__(s) for s in role_conf_relative_files])
                    ]
                    if remove_conf_files:
                        _cmds.append(share.echo_action(role_title, "remove conf"))
                        _cmds.append("sudo rm -rfv {0}".format(" ".join(remove_conf_files)))
            _cmds.append('sudo mkdir -p {1} && sudo cp -rv {0} {1}'.format(
                role_node_target_conf_path if role_node_target_conf_path and role_node_target_conf_path.exists() else role_conf_path.as_posix(),
                target_app_path.as_posix())
            )
        if role_init_sh.exists():
            _cmds.append("bash {}".format(role_init_sh.as_posix()))
        if role_deploy_file.exists():
            if args.debug:
                _cmds.append(docker_compose_cmd("config"))
            up_args = ["up --detach --build --remove-orphans"]
            if args.recreate:
                up_args.append("--force-recreate")
            _cmds.append(docker_compose_cmd(collection_util.flat_to_str(up_args)))
    if args.command == share.Command.delete.value:
        if role_deploy_file.exists():
            _cmds.append(docker_compose_cmd("down --remove-orphans"))

    if args.command == share.Command.build.value and args.target.startswith("Dockerfile"):
        role_dockerfile = role_output_path.joinpath(args.target)
        registry_source_url = role_env['param_registry_url']
        registry_source_dir = role_env['param_registry_dir']
        registry_source_url = path_util.join_path(registry_source_url, registry_source_dir)
        if role_dockerfile.exists():
            registry_source_tag = path_util.join_path(registry_source_url, role_name)
            if args.tag:
                registry_source_tag = registry_source_tag + ":" + args.tag
            registry_targets = args.param.get("param_registry_targets", []).split(",")
            registry_target_tags = []
            for t in registry_targets:
                registry_target_url = role_env.get("param_registry_{0}_url".format(t))
                registry_target_dir = role_env.get("param_registry_{0}_dir".format(t))
                if not registry_target_url:
                    logger.warning("registry_target: {} not exist".format(t))
                    continue
                target_registry_tag = path_util.join_path(registry_target_url, registry_target_dir, role_name)
                if args.tag:
                    target_registry_tag = target_registry_tag + ":" + args.tag
                registry_target_tags.append(target_registry_tag)
            _cmds.append("docker build --tag {0} --file {1} {2} --pull".format(registry_source_tag, role_dockerfile.as_posix(), role_output_path.as_posix()))
            _cmds.extend(["docker tag {} {}".format(registry_source_tag, t) for t in registry_target_tags])
            if args.push:
                _cmds.append("docker push {0}".format(registry_source_tag))
                _cmds.extend(["docker push {0}".format(t) for t in registry_target_tags])
            if registry_targets:
                registry_github_repo: str = role_env["param_registry_github_repo"]
                registry_github_repo_url: urllib3.util.Url = urllib3.util.parse_url(registry_github_repo)
                registry_github_repo_name: str = pathlib.Path(registry_github_repo_url.path).name
                registry_github_repo_dir: pathlib.Path = home_path.joinpath(registry_github_repo_name)
                if not registry_github_repo_dir.exists():
                    share.execute("git clone {0} {1}".format(registry_github_repo.replace("https://github.com", "git@github.com:"), registry_github_repo_dir))
                registry_github_repo_role_dir = registry_github_repo_dir.joinpath(role_name)
                registry_github_repo_role_dir.mkdir(exist_ok=True)
                sync_is_change = file_util.sync(role_output_path,
                                                lambda a: any(regex_util.match_rules(["Dockerfile*", "docker-entrypoint.sh"], a.as_posix()).values()),
                                                registry_github_repo_role_dir)
                if sync_is_change:
                    _cmds.append("cd {0} && git add . && git commit -m \"# add or update {1} Dockerfile\" && git push && cd".format(registry_github_repo_role_dir.as_posix(), role_name))
    return _cmds


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, get_cmds, role_deep=2)
    installer.run(base_deploy_file=root_path.joinpath("deploy.yml"))
