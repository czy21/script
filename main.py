import filecmp
import logging
import pathlib
from server import share
from utility import file as file_util, template as template_util


def collect_doc(source_name):
    source_dir = current.joinpath("server/{0}".format(source_name))
    share.execute("cd {0} && rm -rf build && sh main.sh {1} build --target doc --env-file env-public.yaml --all-namespace".format(source_dir.as_posix(), "local"))
    source_build_dir = source_dir.joinpath("build")
    target_dir = doc_public.joinpath(source_name)
    source_md_names = []
    for s in filter(lambda f: f.is_file(), source_build_dir.rglob("**/output/doc.md")):
        name = s.parent.parent.parent.stem
        t: pathlib.Path = target_dir.joinpath("{}.md".format(name))
        source_md_names.append(name)
        if not t.exists() or not filecmp.cmp(s, t):
            file_util.copy(s, t)
    for t in filter(lambda f: f.is_file(), target_dir.rglob("*")):
        t: pathlib.Path = t
        if not source_md_names.__contains__(t.stem):
            t.unlink(missing_ok=True)
    source_md_names.sort()
    return source_md_names

logger = logging.getLogger()
# sh toolchain.sh -h user@host build --target doc --env-file env-public.yaml --all-namespace
if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    current = pathlib.Path(__file__).parent
    mkdocs = current.joinpath("mkdocs.yaml")
    doc = current.joinpath("doc")
    doc_public = doc.joinpath("public")
    mkdocs_template = doc.joinpath("mkdocs_template.yaml")
    docker_docs=collect_doc("docker")
    chart_docs=collect_doc("chart")
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{
            "param_docker_mds": "\n      - ".join(["{0}: {1}".format(m, "docker/" + m + ".md") for m in docker_docs]),
            "param_chart_mds": "\n      - ".join(["{0}: {1}".format(m, "chart/" + m + ".md") for m in chart_docs])
        }
    )
    file_util.write_text(mkdocs, mkdocs_text)
