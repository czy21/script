import os
from pathlib import Path

import filetype
import numpy
import pandas

if __name__ == '__main__':
    m = os.listdir(Path("P:"))
    suffix = [Path("P:").joinpath(t).suffix for t in m]
    for l in numpy.unique(suffix):
        print(" => ".join([l,str(pandas.DataFrame([a for a in suffix if a == l]).count()[0])]))
    for t in m:
        y=Path("P:").joinpath(t)
        if filetype.guess(y) is None:
            print("aaaafewa")
    # print(numpy.grou(suffix))
    # print("a")
