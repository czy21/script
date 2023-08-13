import pathlib

from utility import file as file_util, template as template_util

# bash toolchain.sh -h user@host build --target doc --env-file env-public.yaml --all-namespace
if __name__ == '__main__':
    current = pathlib.Path(__file__).parent
    mkdocs = current.joinpath("mkdocs.yaml")
    doc = current.joinpath("doc")
    doc_public = doc.joinpath("public")
    mkdocs_template = doc.joinpath("mkdocs_template.yaml")
    container_source_dir = current.joinpath("container")
    container_target_dir = doc_public.joinpath("container")
    container_md_names = []
    for s in filter(lambda f: f.is_file(), container_source_dir.rglob("**/docker.md")):
        name = s.parent.stem
        t: pathlib.Path = container_target_dir.joinpath("{}.md".format(name))
        container_md_names.append(name)
        file_util.copy(s, t)
    container_md_names.sort()
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{"param_container_mds": "\n      - ".join(["{0}: {1}".format(t, "container/" + t + ".md") for t in container_md_names])}
    )
    file_util.write_text(mkdocs, mkdocs_text)
