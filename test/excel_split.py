from pathlib import Path

import pandas as pd
import numpy as np
from pandas import DataFrame


def split_csv(file_path, chunk_size):
    i = 1
    f_path = Path(file_path).resolve()
    f_name = f_path.stem
    with open(f_path, encoding="utf-8") as fv:
        df = pd.read_csv(fv, low_memory=False)
        for chunk in np.array_split(df, len(df) // chunk_size):
            chunk.to_excel(f_path.parent.joinpath("_".join([f_name, str(i)]) + ".xlsx").as_posix(), index=False)
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
    # split_csv("C:/Users/zhaoyu.chen/Desktop/maixin/calllog-2017-01-01~2021-12-01.csv", 100000)
