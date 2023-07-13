import pathlib
from utility import file as file_util, template as template_util

if __name__ == '__main__':
    current_path = pathlib.Path(__file__).parent
    docker_md_path = current_path.joinpath("doc/public/docker")
    docker_md_template = docker_md_path.joinpath("template.md")
    docker_output_deploys = current_path.joinpath("server/docker/build").glob("**/output/deploy.yml")
    for t in docker_output_deploys:
        name = t.parent.parent.parent.stem
        content = file_util.read_text(t)
        md_text = template_util.Template(file_util.read_text(docker_md_template)).render(**{"param_docker_compose_content": content})
        file_util.write_text(docker_md_path.joinpath(name + ".md"), md_text)
