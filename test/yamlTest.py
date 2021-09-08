import io
import shutil
from pathlib import Path

import yaml


def split(root_path: str):
    for d in Path(root_path).iterdir():
        f = d.joinpath("deploy.yaml")
        if f.exists():
            templates_path = d.joinpath("templates")
            shutil.rmtree(path=templates_path, ignore_errors=True)
            templates_path.mkdir(parents=True, exist_ok=True)
            y = yaml.unsafe_load_all(open(f))
            for content in y:
                if content and content["kind"]:
                    kind_path = f.joinpath(templates_path).joinpath(str(content["kind"]).lower() + ".yaml")
                    # with io.open(kind_path, "w+", encoding="utf-8") as y_file:
                        # yaml.dump(content, y_file)
                # if s and s["kind"]:
                #     print(f.parent.name+"   "+ s["kind"])
            # print(f)


if __name__ == '__main__':
    root_path = Path(__file__).joinpath("../../server/pod/db").resolve().as_posix()
    split(root_path)
