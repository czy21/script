import pathlib
import shutil
from uuid import uuid4


def gen():
    src_path = pathlib.Path(__file__).parent.joinpath("dsm")
    dst_path = pathlib.Path(__file__).parent.joinpath("out")
    dst_path.mkdir(exist_ok=True)

    file_stem_id_map = {}
    for t in filter(lambda f: f.is_file(), src_path.rglob("*")):
        t: pathlib.Path = t
        t_lower: pathlib.Path = pathlib.Path(t.as_posix().lower())
        fid = file_stem_id_map.get(t_lower.stem)
        if fid is None:
            fid = uuid4()
            file_stem_id_map[t_lower.stem] = fid

        f_path = dst_path.joinpath("{0}{1}".format(fid, t_lower.suffix))
        if f_path.exists():
            print(t)
        else:
            shutil.move(t, f_path)


if __name__ == '__main__':
    gen()
