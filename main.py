import logging
import pathlib
from utility import file as file_util, template as template_util, regex as regex_util

logger = logging.getLogger()
# bash toolchain.sh -h user@host install --dry-run --all-namespace --env-file env-public.yaml
if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    cwd = pathlib.Path(__file__).cwd()
    doc = cwd.joinpath("doc")
    doc_public = doc.joinpath("public")
    mkdocs = cwd.joinpath("mkdocs.yaml")
    mkdocs_template = cwd.joinpath("mkdocs_template.yaml")
    docker_deploys = cwd.joinpath("server/docker/build")
    docker_md = doc_public.joinpath("docker")
    docker_md_template = doc.joinpath("docker-template.md")
    docker_mds = []
    docker_md_ignore = ["ssl/", "test/", "os"]
    docker_md_ignore.extend(["{0}/build/output".format(t) for t in ["script"]])
    for t in filter(lambda f: f.is_file() and not any(regex_util.match_rules(docker_md_ignore, f.as_posix()).values()),
                    docker_deploys.rglob("**/output/deploy.yml")):
        name = t.parent.parent.parent.stem
        content = file_util.read_text(t)
        md_text = template_util.Template(file_util.read_text(docker_md_template)).render(**{"param_docker_compose_content": content})
        file_util.write_text(docker_md.joinpath(name + ".md"), md_text)
        docker_mds.append(name)
    docker_mds.sort()
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{"param_docker_mds": "\n      - ".join(["{0}: {1}".format(t, "docker/" + t + ".md") for t in docker_mds])}
    )
    file_util.write_text(mkdocs, mkdocs_text)
