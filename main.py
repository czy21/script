import argparse
import logging
import pathlib
import shutil
import requests, re, traceback, json

import server
from util import file as file_util, template as template_util, collection as collection_util, yaml as yaml_util


def collect_doc(root_path, container_path, source_name, target_dir):
    shutil.rmtree(target_dir, ignore_errors=True)
    source_path = root_path.joinpath("server/{0}".format(source_name))
    server.execute(f"cd {source_path.as_posix()};PYTHONPATH={root_path.as_posix()} $HOME/.python3/bin/python3 -B main.py build --target doc --all-namespace --check --clean")
    namespaces = {}
    for sd in filter(lambda f: f.is_file, source_path.rglob("build/doc.md")):
        role_path = sd.parent.parent
        namespace = role_path.parent.name
        role_name = role_path.name
        role_doc_path = sd.parent.joinpath('doc')
        namespaces.setdefault(namespace, []).append({"name": role_name, "file": "{}/{}/{}.md".format(source_name, namespace, role_name)})
        file_util.copy(sd, target_dir.joinpath("{}/{}.md".format(namespace, sd.parent.parent.name)))
        if role_doc_path.exists():
            shutil.copytree(role_doc_path, container_path.joinpath(role_name).joinpath(source_name), dirs_exist_ok=True)
    return [
        {
            "namespace": k,
            "roles": sorted(v, key=lambda x: x.get('name'))
        }
        for k, v in sorted(namespaces.items(), key=lambda x: x)
    ]


def build_doc(root_path):
    container_path = root_path.joinpath('build/container')
    shutil.rmtree(container_path, ignore_errors=True)
    doc = root_path.joinpath("doc")
    doc_public = doc.joinpath("public")
    doc_template = doc.joinpath("mkdocs_template.yaml")
    file_util.write_text(root_path.joinpath("mkdocs.yaml"), template_util.Template(file_util.read_text(doc_template)).render(
        **{
            "param_doc_nav": dict([t.capitalize(), collect_doc(root_path, container_path, t, doc_public.joinpath(t))] for t in ["docker", "chart"])
        }
    ))

if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")

    args = parser.parse_args()

    if args.command == "build":
        build_doc(root_path)