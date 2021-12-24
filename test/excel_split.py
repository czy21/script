from pathlib import Path

import pandas as pd
import numpy as np
from pandas import DataFrame


def split_excel(file_path, chunk_size):
    i = 1
    f_path = Path(file_path).resolve()
    f_name = f_path.stem
    f_suffix = f_path.suffix
    df = pd.read_excel(f_path.as_posix())
    for chunk in np.array_split(df, len(df) // chunk_size):
        chunk.to_excel(f_path.parent.joinpath("_".join([f_name, str(i)]) + f_suffix).as_posix(), index=False)
        i += 1


def count_excel(root_path, pattern):
    count = 0
    for p in Path(root_path).glob(pattern):
        df: DataFrame = pd.read_excel(p.as_posix())
        f_row_count = df.shape[0]
        print(f_row_count)
        count += f_row_count
    print(count)


if __name__ == '__main__':
    count_excel("C:/Users/zhaoyu.chen/Desktop/maixin", "calllog-2017-01-01~2021-12-01_*.xlsx")
    # split_excel("C:/Users/zhaoyu.chen/Desktop/maixin/contact-2017-01-01~2021-12-01.xlsx", 100000)
