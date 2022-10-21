import pathlib

import pandas as pd
from faker import Faker


def write_csv(items, file):
    df = pd.DataFrame(data=items)
    df.to_csv(file, encoding="utf_8_sig", index=False, header=False)


def write_sql(items, file):
    file.write("insert into customer(name,id_num,phone_no) values" + ",".join(["('{0}','{1}','{2}')".format(t["name"], t["id_num"], t["phone_no"]) for t in items]) + ";\n")


def generate(total: int):
    fake: Faker = Faker(locale="zh-CN")
    temp_dir = pathlib.Path(__file__).parent.joinpath("___temp")
    csv_file = temp_dir.joinpath("customer.csv")
    sql_file = temp_dir.joinpath("customer.sql")
    data = []
    with open(sql_file, mode="a", encoding="utf-8", newline="\n") as s:
        with open(csv_file, mode="a", encoding="utf-8", newline="\n") as c:
            for _ in range(0, total):
                user = {
                    "name": fake.name(),
                    "id_num": fake.ssn(min_age=18, max_age=60),
                    "phone_no": fake.phone_number()
                }
                data.append(user)
                if data.__len__() >= 100:
                    write_csv(data, c)
                    write_sql(data, s)
                    data.clear()

            if data.__len__() > 0:
                write_csv(data, c)
                write_sql(data, s)


if __name__ == '__main__':
    generate(10)
