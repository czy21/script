import logging
import pathlib

from utility import file as file_util, template as template_util, regex as regex_util, safe as safe_util, yaml as yaml_util, path as path_util

md_type_yaml = ["yaml", "yml"]


def get_file_type(extension):
    extension = extension.split(".")[1] if extension.split(".").__len__() > 1 else "text"
    if extension in md_type_yaml:
        return "yaml"
    elif extension == "sh":
        return "bash"
    elif extension == "xml":
        return "xml"
    elif extension == "json":
        return "json";
    else:
        return "text"


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
    docker_md_ignore = ["ssl/", "test/", "os/", "go-pulsar-manager", "ndisk", "emby"]
    docker_md_ignore.extend(["{0}/build/output".format(t) for t in ["script"]])
    for t in filter(lambda f: f.is_file() and not any(regex_util.match_rules(docker_md_ignore, f.as_posix()).values()), docker_deploys.rglob("**/output/deploy.yml")):
        role_env_file = t.parent.joinpath("env.yaml")
        role_env = {} | global_env
        if role_env_file.exists():
            role_env |= yaml_util.load(role_env_file)


        def get_registry(n):
            return "/".join([role_env["param_registry_url"], role_env["param_registry_dir"], n])


        name = t.parent.parent.parent.stem
        dockerfile_dict = {t.name: {
            "content": file_util.read_text(t),
            "command": "docker build --tag {0} --file {1} . --pull".format(get_registry("-".join(filter(lambda d: d != "", [name, t.name.replace("Dockerfile", "").lower()]))), t.name)
        } for t in sorted(t.parent.glob("Dockerfile*"), reverse=True)}
        target_path = pathlib.Path(path_util.join_path(role_env["param_docker_data"],
                                                       role_env["param_role_project_name"] if role_env.get("param_role_project_name") else name)
                                   )

        target_conf_dict = {
            path_util.join_path(str(target_path), str(c.relative_to(t.parent))): {
                "content": file_util.read_text(c),
                "fileType": get_file_type(c.suffix)
            }
            for c in
            filter(lambda f: f.is_file() and not any(regex_util.match_rules(["cert", "prometheus", "grafana", "conf.d/app.conf"], f.as_posix()).values()), t.parent.joinpath("conf").rglob("*"))}

        compose_command = "docker-compose --project-name {0} --file docker-compose.yaml up --detach --build --remove-orphans".format(target_path.stem)
        compose_content = file_util.read_text(t)
        md_dst = docker_md.joinpath(name + ".md")
        md_dst_text = template_util.Template(file_util.read_text(docker_md_template)).render(**{
            "param_docker_dockerfile_dict": dockerfile_dict,
            "param_docker_conf_dict": target_conf_dict,
            "param_docker_compose_command": compose_command,
            "param_docker_compose_content": compose_content
        })
        if not md_dst.exists() or (md_dst.exists() and not safe_util.md5_encrypt(file_util.read_text(md_dst)) == safe_util.md5_encrypt(md_dst_text)):
            file_util.write_text(md_dst, md_dst_text)
        docker_mds.append(name)
    docker_mds.extend(["emby"])
    docker_mds.sort()
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{"param_docker_mds": "\n      - ".join(["{0}: {1}".format(t, "docker/" + t + ".md") for t in docker_mds])}
    )
    file_util.write_text(mkdocs, mkdocs_text)
