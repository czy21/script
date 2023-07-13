import pathlib
from utility import file as file_util, template as template_util

if __name__ == '__main__':
    cwd = pathlib.Path(__file__).cwd()
    mkdocs = cwd.joinpath("mkdocs.yaml")
    mkdocs_template = cwd.joinpath("mkdocs_template.yaml")
    docker_deploys = cwd.joinpath("server/docker/build").glob("**/output/deploy.yml")
    docker_md = cwd.joinpath("doc/public/docker")
    docker_md_template = docker_md.joinpath("template.md")
    docker_mds = []
    for t in docker_deploys:
        name = t.parent.parent.parent.stem
        content = file_util.read_text(t)
        md_text = template_util.Template(file_util.read_text(docker_md_template)).render(**{"param_docker_compose_content": content})
        file_util.write_text(docker_md.joinpath(name + ".md"), md_text)
        docker_mds.append(name)
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{"param_docker_mds": "\n      - ".join(["{0}: {1}".format(t, "docker/" + t + ".md") for t in docker_mds])}
    )
    file_util.write_text(mkdocs, mkdocs_text)
