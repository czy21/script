import datetime
import json
from pathlib import Path

import pandas as pd
from faker import Faker


def generate():
    fake: Faker = Faker(locale="zh-CN")
    columns = [
        '经销商代码',
        '*经销商名称',
        '客户代码',
        '*客户名称',
        '产品代码',
        '*产品名称',
        '*产品规格',
        '*数量',
        '*单位',
        '单价',
        '金额',
        '订单日期'
    ]
    products = ["第{0}个产品".format(t) for t in range(0, 10000)]
    product_units = ["什么{0}规格".format(t) for t in range(0, 10000)]
    data = []
    for t in range(0, 100000000):
        data.append([
            fake.ean(length=13),  # from_institution_code
            fake.company(),  # from_institution_name
            fake.ean(length=13),  # to_institution_code
            fake.company(),  # to_institution_name
            fake.ean(length=13),  # product_code
            fake.words(1, products)[0],  # product_name
            fake.company(),  # product_spec
            str(fake.pydecimal(right_digits=4, min_value=20, max_value=200)),  # product_quantity
            fake.words(1, product_units)[0],  # product_unit
            str(fake.pydecimal(right_digits=4, min_value=20, max_value=200)),  # product_price
            str(fake.pydecimal(right_digits=4, min_value=20, max_value=200)),  # product_amount
            str(fake.date_between(start_date=datetime.date.fromisoformat("2000-01-01"),
                                  end_date=datetime.date.fromisoformat("2021-12-01")))
        ])
        df = pd.DataFrame(data=data, columns=columns)
        df.to_excel(Path("c:/Users/zhaoyu.chen/Desktop/1M.xlsx"), index=False)


if __name__ == '__main__':
    # test()
    generate()
