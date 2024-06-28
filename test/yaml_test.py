import pathlib
import sys

import yaml

from utility import yaml as yaml_util

if __name__ == '__main__':
    code="@CheckExcelData(isCheckNumber = true)\n@ExcelProperty(value = {{\"{0}月小计\", \"费用金额\"}},index={1})\nprivate String m{0};\n"
    for t in range(1,13):
        print(code.format(t,15+t-1))

