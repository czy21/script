import filecmp
import logging
import pathlib,json,shutil
from server import share
from utility import file as file_util, template as template_util


def collect_doc(source_name):
    source_dir = current.joinpath("server/{0}".format(source_name))
    share.execute("cd {0} && rm -rf build && sh main.sh {1} build --target doc --env-file env-public.yaml --all-namespace".format(source_dir.as_posix(), "local"))
    source_build_dir = source_dir.joinpath("build")
    target_dir = doc_public.joinpath(source_name)
    shutil.rmtree(target_dir,ignore_errors=True)
    namespaces = []
    for s in filter(lambda f: f.is_dir(),source_build_dir.iterdir()):
        roles=[]
        for sd in filter(lambda f: f.is_file, s.rglob("**/output/doc.md")):
            t: pathlib.Path = target_dir.joinpath("{}/{}.md".format(s.name,sd.parent.parent.parent.name))
            role_name=sd.parent.parent.parent.name
            roles.append({"name": role_name,"file": "{}/{}/{}.md".format(source_name,s.name,role_name)})
            file_util.copy(sd, t)
        roles.sort(key=lambda k: k.get('name'))
        if roles:
          namespaces.append({"namespace":s.name,"roles":roles})
    namespaces.sort(key=lambda k: k.get('namespace'))
    return namespaces

logger = logging.getLogger()
# sh toolchain.sh -h user@host build --target doc --env-file env-public.yaml --all-namespace
if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    current = pathlib.Path(__file__).parent
    mkdocs = current.joinpath("mkdocs.yaml")
    doc = current.joinpath("doc")
    doc_public = doc.joinpath("public")
    mkdocs_template = doc.joinpath("mkdocs_template.yaml")
    mkdocs_text = template_util.Template(file_util.read_text(mkdocs_template)).render(
        **{
            "param_doc_nav": dict([t.capitalize(),collect_doc(t)] for t in ["docker","chart"])
        }
    )
    file_util.write_text(mkdocs, mkdocs_text)
