import pathlib

import yaml

if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent.joinpath("___temp/a.yaml"), encoding="utf-8") as f:
        a = yaml.full_load(f)
        print("a")
