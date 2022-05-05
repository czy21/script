import io
import os
import shutil
import sys
from pathlib import Path

from ruamel import yaml


def _str_representer(dumper: yaml.Dumper, data):
    style = ''
    if '\n' in data:
        style = '|'
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style)


yaml.RoundTripRepresenter.add_representer(str, _str_representer)


def split(root_path: str):
    rp = Path(root_path)
    for d in rp.iterdir():
        f = d.joinpath("deploy.yaml")
        if f.exists():
            chart_path = d.joinpath("Chart.yaml")
            shutil.rmtree(path=chart_path, ignore_errors=True)
            chart_content = {
                "apiVersion": "v2",
                "name": d.name,
                "version": "0.1.0"
            }
            values_path = d.joinpath("values.yaml")
            shutil.rmtree(path=chart_path, ignore_errors=True)
            values_content = {
                "namespace": rp.name
            }
            with io.open(values_path, "w+", encoding="utf-8", newline="\n") as v_file:
                yaml.dump(values_content, v_file, default_flow_style=False)
            with io.open(chart_path, "w+", encoding="utf-8", newline="\n") as c_file:
                yaml.dump(chart_content, c_file, default_flow_style=False)
            templates_path = d.joinpath("templates")
            shutil.rmtree(path=templates_path, ignore_errors=True)
            templates_path.mkdir(parents=True, exist_ok=True)
            fo = open(f, "r", encoding="utf-8", newline="\n")
            y = yaml.load_all(fo, Loader=yaml.UnsafeLoader)
            template_deploy_path = f.joinpath(templates_path).joinpath("deploy.yaml")
            with io.open(template_deploy_path, "w+", encoding="utf-8", newline="\n") as y_file:
                all_doc = []
                for content in y:
                    if content and content["kind"]:
                        if "namespace" in content["metadata"].keys():
                            content["metadata"]["namespace"] = "{{ .Values.namespace }}"
                    all_doc.append(content)
                yaml.dump_all(all_doc, y_file, Dumper=yaml.RoundTripDumper, default_flow_style=False, explicit_start=True)
            fo.close()
            os.remove(f)


def self_ref():

    with open(Path(__file__).joinpath("../___temp/a.yml").resolve().as_posix(), mode="r", encoding="utf-8") as f:
        obj = yaml.load(f, yaml.UnsafeLoader)
        print(obj)


if __name__ == '__main__':
    self_ref()
    # split(Path(__file__).joinpath("../../server/pod/app").resolve().as_posix())
    # split(Path(__file__).joinpath("../../server/pod/db").resolve().as_posix())
    # split(Path(__file__).joinpath("../../server/pod/init").resolve().as_posix())
    # split(Path(__file__).joinpath("../../server/pod/ops").resolve().as_posix())
    # split(Path(__file__).joinpath("../../server/pod/erp").resolve().as_posix())
