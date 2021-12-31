import json

import pandas as pd


def resolve_follow(p: str):
    with pd.ExcelFile(path_or_buffer=p) as f:
        df_dict = pd.read_excel(f, sheet_name="Sheet1").T
        values = []
        l1 = ""
        l2 = ""
        for d in df_dict.items():
            cl1 = d[1]["一级菜单"]
            cl2 = d[1]["二级菜单"]
            cl3 = d[1]["三级菜单"]
            val = {}
            if not pd.isna(cl1):
                l1 = cl1
            if not pd.isna(cl2):
                l2 = cl2
            val["name"] = cl3
            val["l2"] = l2
            val["l1"] = l1
            values.append(val)
        #     for l1 in d[1]:
        #         print(i)
        # if not pd.isna(d):
        # values.append(l1)
        print(json.dumps(values,ensure_ascii=False))
        # print(d)


# def recursive_dict():


if __name__ == '__main__':
    resolve_follow("C:\\Users\\zhaoyu.chen\\Desktop\mx\\电话服务小结节点1213.xlsx")
