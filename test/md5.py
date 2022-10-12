import itertools
import pathlib


# find . -maxdepth 1 -type f -exec md5sum {} \; | sort > md5-$(date +%Y%m%d-%H%M).txt
def repeat(md5_file: pathlib.Path):
    with open(md5_file, encoding="utf-8", newline="\n") as f:
        data = [{"name": t.strip().split("  ./")[1], "md5": t.strip().split("  ./")[0]} for t in iter(f.readline, '')]
        repeats = []
        removes = []
        for k, v in itertools.groupby(list(sorted(data, key=lambda a: a["md5"])), key=lambda a: a["md5"]):
            values = list(v)
            if values.__len__() > 1:
                repeats.append({k: list(map(lambda a: a["name"], values))})
        print("repeat:")
        for t in repeats:
            print(t)
        print("removes:")
        for t in repeats:
            for k, v in t.items():
                v.pop(0)
                removes.extend(v)
        print("size: {}".format(removes.__len__()))
        print(" ".join(removes))


if __name__ == '__main__':
    md5_file = pathlib.Path(__file__).parent.joinpath("___temp/md5-20221011-1801.txt")
    repeat(md5_file)
