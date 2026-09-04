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

        self.container_compose = f"{self.gen_sudo()} docker compose"
        if self.context.role_env.get("param_container_engine") == 'podman':
            self.container_compose = "podman compose"

        self.root_compose_file = context.root_path.joinpath("compose.yml")
        self.root_doc_template_file = context.root_path.joinpath("doc-template.md")

        self.role_deploy_env_file = context.role_out_path.joinpath(".env")
        self.role_compose_file = context.role_out_path.joinpath("compose.yml")
        self.role_deploy_swarm_file = context.role_out_path.joinpath("compose-swarm.yml")

        self.role_conf_path = context.role_out_path.joinpath("conf")
        self.role_init_sh = context.role_out_path.joinpath("init.sh")

        self.role_node_target_conf_path = self.context.role_node_target_path.joinpath("conf")
        self.role_node_target_deploy_file = self.context.role_node_target_path.joinpath("compose.yml")

        self.role_project_name = self.context.role_env.get("param_role_project_name", self.context.role_name)
        self.role_target_path = pathlib.Path(self.context.role_env.get("param_role_target_path", self.context.role_env.get("param_docker_data") + "/" + self.context.role_name))
        if self.role_target_path.parents.__len__() <= 1:
            raise Exception('role_target_path: {} parents length <= 1'.format(self.role_target_path))
        self.role_target_conf_path = self.role_target_path.joinpath("conf")
    
    def gen_sudo(self):
        self.container_sudo = self.context.role_env.get("param_container_sudo",True)
        return "sudo" if self.container_sudo else ""

    def compose_cmd(self, project_name, option):
        role_compose_files = []
        if self.context.role_env.get('param_include_root_compose',True):
            role_compose_files.append(self.root_compose_file.as_posix())
        role_compose_files.append(self.role_compose_file.as_posix())
        if self.role_node_target_deploy_file.exists():
            role_compose_files.append(self.role_node_target_deploy_file)
        cmd = [
            self.container_compose
        ]
        env_file = self.context.role_out_path.joinpath('.env')
        if self.container_compose == 'podman compose' and env_file.exists():
            cmd.append(f'--env-file {env_file.as_posix()}')

        cmd.append(f'--progress plain --project-name {project_name}')
        cmd.append(" ".join(["--file {0}".format(t) for t in role_compose_files]))
        cmd.append(option)

        cmd = collection_util.flat_to_str(cmd)
        return f'(cd {self.context.role_out_path.as_posix()};{cmd})'

    def install(self) -> list[str]:
        _cmds = []
        if self.role_conf_path.exists() or self.role_node_target_conf_path.exists():
            if self.context.args.rm_conf and self.role_target_conf_path.exists():
                _cmds.append("{0} rm -rfv {1}".format(self.gen_sudo(),self.role_target_conf_path.as_posix()))
            _cmds.append('{0} mkdir -p {2} && {0} cp -rv {1} {2}'.format(self.gen_sudo(),self.role_conf_path.as_posix(),self.role_target_path.as_posix()))
        if self.role_init_sh.exists():
            _cmds.append("bash {}".format(self.role_init_sh.as_posix()))
        if self.role_compose_file.exists():
            if self.context.args.debug:
                _cmds.append(self.compose_cmd(self.role_project_name,"config"))
            if self.context.role_env.get("param_swarm",False):
                _cmds.append(self.compose_cmd('swarm',f"config | sed '/^name: swarm/d' > {self.role_deploy_swarm_file.as_posix()}"))
                _cmds.append(f"docker stack deploy -c {self.role_deploy_swarm_file.as_posix()} {self.role_project_name}")
            else:
                up_args = ["up --detach --build --remove-orphans"]
                if self.context.args.recreate:
                    up_args.append("--force-recreate")
                _cmds.append(self.compose_cmd(self.role_project_name,collection_util.flat_to_str(up_args)))
        return _cmds

    def build(self) -> list[str]:
        _cmds = []
        registry_source_url = self.context.role_env.get('param_registry')
        registry_source_dir = self.context.role_env.get('param_registry_dir')

        role_versions = self.context.role_env.get('param_role_versions')

        if role_versions:
            for role_version in role_versions:
                role_version['Dockerfile'] = self.context.role_out_path / 'Dockerfile'
                role_version['build_args'] = f"--build-arg BASE_IMAGE={role_version.get('from')}"
        else:
            role_versions = [
                {
                    'Dockerfile': t,
                    'name': "-".join(filter(lambda d: d != "", [self.context.role_name, t.name.replace("Dockerfile", "").lower()]))
                }
                for t in sorted(self.context.role_out_path.glob(self.context.args.target), reverse=True)
            ]
        if self.context.args.target.startswith("Dockerfile"):
            for t in role_versions:
                registry_source_tag = self.get_image_tag(registry_source_url, registry_source_dir, t.get('name'))
                registry_targets = self.context.args.param.get("param_registry_targets").split(",") if self.context.args.param.get("param_registry_targets") else []
                registry_target_tags = []
                for r in registry_targets:
                    registry_target_url = self.context.role_env.get("param_registry_target_{0}".format(r))
                    registry_target_dir = self.context.role_env.get("param_registry_target_{0}_dir".format(r))
                    if not registry_target_url:
                        logger.warning("registry target: {} not exist".format(r))
                        continue
                    registry_target_tag = self.get_image_tag(registry_target_url, registry_target_dir, t.get('name'))
                    registry_target_tags.append((r, registry_target_tag))
                _cmds.append(f"docker build {t.get('build_args','')} --tag {registry_source_tag} --file {t.get('Dockerfile').as_posix()} {self.context.role_out_path.as_posix()} --pull")
                _cmds.extend([f"docker tag {registry_source_tag} {t[1]}" for t in registry_target_tags])
                if self.context.args.push:
                    if not registry_target_tags:
                        _cmds.append(f"docker push {registry_source_tag}")
                    _cmds.extend([f"docker --config $HOME/.docker/registry/{t[0]} push {t[1]}" for t in registry_target_tags])
        if self.context.args.target == "doc":
            if self.any_doc_exclude(self.context.role_out_path):
                registry_git_repo_raw_format = self.context.role_env.get("param_registry_git_repo_raw") + "/main/{0}/docker/{1}"
                md_param = {
                    "param_registry_git_repo_dict": {t["name"]: "{}/{}/{}".format(t["url"], "tree/main", self.context.role_name) for t in self.context.role_env.get("param_registry_git_repos")},
                    "param_docker_dockerfiles": [
                        {
                            "name": t.name,
                            "command": "docker build --tag {0} --file {1} . --pull".format(self.get_image_tag(registry_source_url, registry_source_dir, "-".join(filter(lambda d: d != "", [self.context.role_name, t.name.replace("Dockerfile", "").lower()]))), t.name),
                            "rawUrl": registry_git_repo_raw_format.format(self.context.role_name, t.name)
                        } for t in sorted(self.context.role_out_path.glob("Dockerfile*"), reverse=True)
                    ],
                    "param_docker_compose": {
                        "name": self.role_compose_file.name,
                        "command": self.container_compose + " --project-name {0} --file compose.yml up --detach --remove-orphans".format(self.role_project_name),
                        "rawUrl": registry_git_repo_raw_format.format(self.context.role_name, self.role_compose_file.name)
                    } if self.role_compose_file.exists() else None
                }
                
                if md_param.get("param_docker_dockerfiles"):
                    if self.context.role_env.get('param_role_versions'):
                        md_param.get("param_docker_dockerfiles")[0]['command'] = "\n".join([
                            "docker build {0} --tag {1} --file {2} . --pull".format(t.get('build_args',''), self.get_image_tag(registry_source_url, registry_source_dir, t.get('name')), 'Dockerfile')
                            for t in role_versions
                        ])
                    else:
                      file_util.write_text(self.context.role_out_path.joinpath("version"), self.context.role_env.get("param_role_version", "latest"))
                md_content = template_util.Template(file_util.read_text(self.root_doc_template_file)).render(**md_param)
                role_readme = self.context.role_out_path.joinpath("README.md")
                file_util.write_text(self.context.role_out_path.joinpath("doc.md"), md_content + "\n" + (file_util.read_text(role_readme) if role_readme.exists() else ""))
            self.sync_to_git_repo("docker")
        return _cmds

    def get_image_tag(self, registry_url, registry_dir, image_name):
        image_name = path_util.join_path(registry_url, registry_dir, image_name)
        image_tag = self.context.args.tag or self.context.role_env.get("param_role_version", "latest")
        return f"{image_name}:{image_tag}"

    def delete(self) -> list[str]:
        _cmds = []
        if self.role_compose_file.exists():
            _cmds.append(self.compose_cmd("down --remove-orphans"))
        return _cmds

    def backup(self) -> list[str]:
        return []

    def restore(self) -> list[str]:
        return []

    def push(self) -> list[str]:
        return []

    def get_merge_ignore_pattern(self):
        return ["compose.yml"]


if __name__ == '__main__':
    share.Installer(pathlib.Path(__file__).parent, DockerRole, role_deep=2).run()
