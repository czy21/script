import io
import os
import shutil
from pathlib import Path

from ruamel import yaml


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
            with io.open(values_path, "w+", encoding="utf-8") as v_file:
                yaml.dump(values_content, v_file, default_flow_style=False)
            with io.open(chart_path, "w+", encoding="utf-8") as c_file:
                yaml.dump(chart_content, c_file, default_flow_style=False)
            templates_path = d.joinpath("templates")
            shutil.rmtree(path=templates_path, ignore_errors=True)
            templates_path.mkdir(parents=True, exist_ok=True)
            fo = open(f, "r", encoding="utf-8")
            y = yaml.load_all(fo, Loader=yaml.UnsafeLoader)
            for content in y:
                if content and content["kind"]:
                    kind_path = f.joinpath(templates_path).joinpath(str(content["kind"]).lower() + ".yaml")
                    with io.open(kind_path, "w+", encoding="utf-8") as y_file:
                        yaml.dump(content, y_file, default_flow_style=False)
            fo.close()
            os.remove(f)


if __name__ == '__main__':
    root_path = Path(__file__).joinpath("../../server/pod/db").resolve().as_posix()
    split(root_path)
