import itertools
import json
import pathlib


def to_json(repos: list):
    group_by_format = {k: sorted(repos, key=lambda t: "-".join([t["type"], t["name"]]))
                       for k, v in itertools.groupby(sorted(repos, key=lambda t: t["format"]), key=lambda a: a["format"])}
    print(json.dumps(group_by_format))


if __name__ == '__main__':
    nexus_file = pathlib.Path(__file__).parent.joinpath("___temp/nexus_1665478533913.json")
    with open(nexus_file, mode="r", encoding="utf-8") as mf:
        repos = json.load(mf)
    to_json(repos)
