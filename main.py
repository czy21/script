import filecmp
import logging
import pathlib

from utility import file as file_util, template as template_util

logger = logging.getLogger()
# bash toolchain.sh -h user@host build --target doc --env-file env-public.yaml --all-namespace
if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    current = pathlib.Path(__file__).parent
    mkdocs = current.joinpath("mkdocs.yaml")
    doc = current.joinpath("doc")
    doc_public = doc.joinpath("public")
    mkdocs_template = doc.joinpath("mkdocs_template.yaml")
    docker_deploys = current.joinpath("server/docker/build")
    docker_md_dir = doc_public.joinpath("docker")
    docker_md_names = []
    for s in filter(lambda f: f.is_file(), docker_deploys.rglob("**/output/doc.md")):
        name = s.parent.parent.parent.stem
        t: pathlib.Path = docker_md_dir.joinpath("{}.md".format(name))
        docker_md_names.append(name)
        if not t.exists() or (not filecmp.cmp(s, t)):
            file_util.copy(s, t)
    for t in filter(lambda f: f.is_file(), docker_md_dir.rglob("*")):
        t: pathlib.Path = t
        if not docker_md_names.__contains__(t.stem):
            t.unlink(missing_ok=True)
    docker_md_names.sort()
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{"param_docker_mds": "\n      - ".join(["{0}: {1}".format(t, "docker/" + t + ".md") for t in docker_md_names])}
    )
    file_util.write_text(mkdocs, mkdocs_text)
