import logging
import pathlib
import shutil

from utility import file as file_util, template as template_util, regex as regex_util, safe as safe_util, yaml as yaml_util, path as path_util

logger = logging.getLogger()
# bash toolchain.sh -h user@host install --dry-run --all-namespace --env-file env-public.yaml
if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    current = pathlib.Path(__file__).parent
    global_env = yaml_util.load(current.joinpath("server/env-public.yaml"))
    mkdocs = current.joinpath("mkdocs.yaml")
    doc = current.joinpath("doc")
    doc_public = doc.joinpath("public")
    mkdocs_template = doc.joinpath("mkdocs_template.yaml")
    docker_deploys = current.joinpath("server/docker/build")
    docker_md = doc_public.joinpath("docker")
    docker_md_template = doc.joinpath("docker-template.md")
    docker_mds = []
    docker_md_ignore = ["ssl/", "test/", "os/"]
    docker_md_ignore.extend(["{0}/build/output".format(t) for t in ["script"]])
    for t in filter(lambda f: f.is_file() and not any(regex_util.match_rules(docker_md_ignore, f.as_posix()).values()), docker_deploys.rglob("**/output/deploy.yml")):
        role_env_file = t.parent.joinpath("env.yaml")
        role_env = {} | global_env
        if role_env_file.exists():
            role_env |= yaml_util.load(role_env_file)
        name = t.parent.parent.parent.stem
        target_path = pathlib.Path(path_util.join_path(role_env["param_docker_data"],
                                                       role_env["param_role_project_name"] if role_env.get("param_role_project_name") else name)
                                   )
        target_conf = path_util.join_path(str(target_path), "conf")
        target_conf_dict = {path_util.join_path(target_conf, c.name): file_util.read_text(c)
                            for c in
                            filter(lambda f: f.is_file() and not any(regex_util.match_rules(["cert", "prometheus", "grafana"], f.as_posix()).values()), t.parent.joinpath("conf").rglob("*"))}
        compose_command = "docker-compose --project-name {0} --file docker-compose.yaml up --detach --build --remove-orphans".format(target_path.stem)
        compose_content = file_util.read_text(t)
        md_dst = docker_md.joinpath(name + ".md")
        md_dst_text = template_util.Template(file_util.read_text(docker_md_template)).render(**{"param_docker_conf_dict": target_conf_dict,
                                                                                                "param_docker_compose_command": compose_command,
                                                                                                "param_docker_compose_content": compose_content})
        if not md_dst.exists() or (md_dst.exists() and not safe_util.md5_encrypt(file_util.read_text(md_dst)) == safe_util.md5_encrypt(md_dst_text)):
            file_util.write_text(md_dst, md_dst_text)
        docker_mds.append(name)
    # remove exists
    for t in [t for t in docker_md.rglob("*") if t.is_file()]:
        if t.stem not in docker_mds:
            t.unlink()
    docker_mds.sort()
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{"param_docker_mds": "\n      - ".join(["{0}: {1}".format(t, "docker/" + t + ".md") for t in docker_mds])}
    )
    file_util.write_text(mkdocs, mkdocs_text)
