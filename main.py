import json
import os
import shutil

import argparse
import pathlib

import server
from util import file as file_util


def collect_doc(root_path, container_path, source_name, target_dir):
    shutil.rmtree(target_dir, ignore_errors=True)
    source_path = root_path.joinpath("server/{0}".format(source_name))
    server.execute(f"PYTHONPATH={root_path.as_posix()} $HOME/.python3/{'Scripts' if os.name == 'nt' else 'bin'}/python3 -B {source_path.as_posix()}/main.py build --roles all --target doc --clean --check --parallel")
    namespaces = {}
    for sd in filter(lambda f: f.is_file, source_path.rglob("build/doc.md")):
        role_path = sd.parent.parent
        namespace = role_path.parent.name
        role_name = role_path.name
        role_repositories_file = sd.parent.joinpath('repositories.json')
        role_doc_path = sd.parent.joinpath('doc')
        file_util.copy(sd, target_dir.joinpath("{}/{}.md".format(namespace, sd.parent.parent.name)))
        if role_doc_path.exists():
            shutil.copytree(role_doc_path, container_path.joinpath(role_name).joinpath(source_name), dirs_exist_ok=True)

        role_doc_dict = {"text": role_name, "link": "{}/{}/{}.md".format(source_name, namespace, role_name)}
        if role_repositories_file.exists():
            with role_repositories_file.open("r", encoding="utf-8") as f:
                role_doc_dict['repositories'] = json.load(f)
        namespaces.setdefault(namespace, []).append(role_doc_dict)
    return {
        'text': source_name.capitalize(),
        'collapsed': True,
        'items': [
            {
                'text': k,
                'collapsed': True,
                'items': sorted(v, key=lambda x: x.get('text'))
            }
            for k, v in sorted(namespaces.items(), key=lambda x: x)
        ]
    }

def build_doc(root_path):
    container_path = root_path / 'build/container'
    doc = root_path.joinpath("doc")
    doc_server_path = doc.joinpath("server")
    doc_server_json = root_path / 'build/doc-server.json'
    file_util.write_text(
        doc_server_json,
        json.dumps([collect_doc(root_path, container_path, t, doc_server_path.joinpath(t)) for t in ["docker", "chart"]])
    )


if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")

    args = parser.parse_args()

    if args.command == "build":
        build_doc(root_path)
