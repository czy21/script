import itertools
import json
import pathlib

exclude_keys = ["httpClient", "storage", "cleanup", "negativeCache", "routingRuleName", "online", "proxy", "docker", "format", "component"]


def order_by_repos(repos):
    rets = []
    for t in sorted(repos, key=lambda t: "-".join([t["type"], t["name"]])):
        for attr in list(filter(lambda a: exclude_keys.__contains__(a), t.keys())):
            if attr == "proxy":
                t["proxy"] = {"remoteUrl": t["proxy"]["remoteUrl"]}
            else:
                t.__delitem__(attr)
        rets.append(t)
    return rets


def to_json(repos: list):
    group_by_format = {k: order_by_repos(v)
                       for k, v in itertools.groupby(sorted(repos, key=lambda t: t["format"]), key=lambda a: a["format"])}
    print(json.dumps(group_by_format))


if __name__ == '__main__':
    nexus_file = pathlib.Path(__file__).parent.joinpath("___temp/nexus.json")
    with open(nexus_file, mode="r", encoding="utf-8") as mf:
        repos = json.load(mf)
    to_json(repos)
