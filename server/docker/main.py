#!/usr/bin/env python3

import logging
import pathlib

from server import share
from utility import (
    collection as collection_util,
    path as path_util,
    file as file_util,
    template as template_util
)

logger = logging.getLogger()


class DockerRole(share.AbstractRole):

    def __init__(self,context:share.RoleContext) -> None:
        super().__init__(context)
        self.root_deploy_file = context.root_path.joinpath("deploy.yml")
        self.root_doc_template_file = context.root_path.joinpath("doc-template.md")

        self.role_deploy_file = context.role_output_path.joinpath("deploy.yml")
        self.role_conf_path = context.role_output_path.joinpath("conf")
        self.role_init_sh = context.role_output_path.joinpath("init.sh")

        self.role_node_target_conf_path = self.context.role_node_target_path.joinpath("conf")
        self.role_node_target_deploy_file = self.context.role_node_target_path.joinpath("deploy.yml")

        self.role_target_path = pathlib.Path(self.context.role_env.get("param_role_target_path", self.context.role_env.get("param_docker_data") + "/" + self.context.role_name))
        if self.role_target_path.parents.__len__() <= 1:
            raise Exception('role_target_path: {} parents length <= 1'.format(self.role_target_path))
        self.role_target_conf_path = self.role_target_path.joinpath("conf")

    def docker_compose_cmd(self, option):
        role_deploy_files = [
            self.root_deploy_file,
            self.role_deploy_file.as_posix()
        ]
        if self.role_node_target_deploy_file.exists():
            role_deploy_files.append(self.role_node_target_deploy_file)
        role_project_name = self.context.role_env.get("param_role_project_name", self.context.role_name)
        return 'sudo docker-compose --project-name {0} {1} {2}'.format(role_project_name, " ".join(["--file {0}".format(t) for t in role_deploy_files]), option)

    def install(self) -> list[str]:
        _cmds = []
        if self.role_conf_path.exists() or self.role_node_target_conf_path.exists():
            if self.context.args.rm_conf and self.role_target_conf_path.exists():
                _cmds.append("sudo rm -rfv {0}".format(self.role_target_conf_path.as_posix()))
            _cmds.append('sudo mkdir -p {1} && sudo cp -rv {0} {1}'.format(
                self.role_node_target_conf_path if self.role_node_target_conf_path.exists() else self.role_conf_path.as_posix(),
                self.role_target_path.as_posix())
            )
        if self.role_init_sh.exists():
            _cmds.append("bash {}".format(self.role_init_sh.as_posix()))
        if self.role_deploy_file.exists():
            if self.context.args.debug:
                _cmds.append(self.docker_compose_cmd("config"))
            up_args = ["up --detach --build --remove-orphans"]
            if self.context.args.recreate:
                up_args.append("--force-recreate")
            _cmds.append(self.docker_compose_cmd(collection_util.flat_to_str(up_args)))
        return _cmds

    def build(self) -> list[str]:
        _cmds = []
        registry_source_url = self.context.role_env.get('param_registry_url')
        registry_source_dir = self.context.role_env.get('param_registry_dir')
        if self.context.args.target.startswith("Dockerfile"):
            for rd in sorted(self.context.role_output_path.glob(self.context.args.target), reverse=True):
                registry_source_tag = self.get_image_tag(registry_source_url, registry_source_dir, rd)
                registry_targets = self.context.args.param.get("param_registry_targets").split(",") if self.context.args.param.get("param_registry_targets") else []
                registry_target_tags = []
                for t in registry_targets:
                    registry_target_url = self.context.role_env.get("param_registry_{0}_url".format(t))
                    registry_target_dir = self.context.role_env.get("param_registry_{0}_dir".format(t))
                    if not registry_target_url:
                        logger.warning("registry target: {} not exist".format(t))
                        continue
                    registry_target_tag = self.get_image_tag(registry_target_url, registry_target_dir, rd)
                    registry_target_tags.append((t, registry_target_tag))
                _cmds.append("docker build --tag {0} --file {1} {2} --pull".format(registry_source_tag, rd.as_posix(), self.context.role_output_path.as_posix()))
                _cmds.extend(["docker tag {} {}".format(registry_source_tag, t[1]) for t in registry_target_tags])
                if self.context.args.push:
                    _cmds.append("docker push {0}".format(registry_source_tag))
                    _cmds.extend(["docker --config $HOME/.docker/{0} push {1}".format(t[0], t[1]) if "dockerhub" == t[0] else "docker push {0}".format(t[1]) for t in registry_target_tags])
        if self.context.args.target == "doc":
            if self.any_doc_exclude(self.context.role_output_path):
                registry_git_repo_raw_format = self.context.role_env.get("param_registry_git_repo_raw") + "/main/{0}/docker/{1}"
                md_param = {
                    "param_registry_git_repo_dict": {t["name"]: "{}/{}/{}".format(t["url"], "tree/main", self.context.role_name) for t in self.context.role_env.get("param_registry_git_repos")},
                    "param_docker_dockerfiles": [
                        {
                            "name": t.name,
                            "command": "docker build --tag {0} --file {1} . --pull".format(self.get_image_tag(registry_source_url, registry_source_dir, t), t.name),
                            "rawUrl": registry_git_repo_raw_format.format(self.context.role_name, t.name)
                        } for t in sorted(self.context.role_output_path.glob("Dockerfile*"), reverse=True)
                    ],
                    "param_docker_compose": {
                        "name": self.role_deploy_file.name,
                        "command": "docker-compose --project-name {0} --file deploy.yml up --detach --remove-orphans".format(self.context.role_env.get("param_role_project_name", self.context.role_name)),
                        "rawUrl": registry_git_repo_raw_format.format(self.context.role_name, self.role_deploy_file.name)
                    } if self.role_deploy_file.exists() else None
                }
                md_content = template_util.Template(file_util.read_text(self.root_doc_template_file)).render(**md_param)
                role_readme = self.context.role_output_path.joinpath("README.md")
                file_util.write_text(self.context.role_output_path.joinpath("doc.md"), md_content + "\n" + (file_util.read_text(role_readme) if role_readme.exists() else ""))
                if md_param.get("param_docker_dockerfiles"):
                    file_util.write_text(self.context.role_output_path.joinpath("image-version"), self.context.role_env.get("param_role_image_version", "latest"))
            self.sync_to_git_repo("docker")
        return _cmds

    def get_image_tag(self, registry_url, registry_dir, role_dockerfile):
        image_tag = path_util.join_path(
            registry_url, registry_dir,
            "-".join(filter(lambda d: d != "", [self.context.role_name, role_dockerfile.name.replace("Dockerfile", "").lower()])))
        image_version = self.context.args.tag if self.context.args.tag else self.context.role_env.get("param_role_image_version")
        return image_tag + ":" + (image_version if image_version else "latest")

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

    def get_merge_ignore_pattern(self):
        return ["deploy.yml"]


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, DockerRole, role_deep=2).run()
