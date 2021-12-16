import datetime
import json
from pathlib import Path

from faker import Faker


def generate():
    fake: Faker = Faker(locale="zh-CN")
    met_file_column_mapping_path = Path(__file__).parent.joinpath("met_file_column_mapping.json")
    with open(met_file_column_mapping_path.as_posix(), "r", encoding="utf-8") as mf:
        met_file_column_list = json.load(mf)
    sale_mapping = next(filter(lambda t: t["tableName"] == "ent_sale", met_file_column_list))
    sale_insert = "insert into ent_sale(" \
                  "from_institution_code," \
                  "from_institution_name," \
                  "to_institution_code," \
                  "to_institution_name," \
                  "product_code," \
                  "product_name," \
                  "product_spec," \
                  "product_quantity," \
                  "product_unit," \
                  "product_price," \
                  "product_amount," \
                  "order_date," \
                  "id) values({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12});"
    products = ["第{0}个产品".format(t) for t in range(0, 10000)]
    product_units = ["什么{0}规格".format(t) for t in range(0, 10000)]
    with open(Path(__file__).parent.joinpath("___temp/sql.sql"), "w+", encoding="utf-8", newline="\n") as sf:
        for t in range(0, 100000000):
            sf.write(u'{}'.format("".join(
                [
                    sale_insert.format(repr(fake.ean(length=13)),  # from_institution_code
                                       repr(fake.company()),  # from_institution_name
                                       repr(fake.ean(length=13)),  # to_institution_code
                                       repr(fake.company()),  # to_institution_name
                                       repr(fake.ean(length=13)),  # product_code
                                       repr(fake.words(1, products)[0]),  # product_name
                                       repr(fake.company()),  # product_spec
                                       repr(str(fake.pydecimal(right_digits=4, min_value=20, max_value=200))),  # product_quantity
                                       repr(fake.words(1, product_units)[0]),  # product_unit
                                       repr(str(fake.pydecimal(right_digits=4, min_value=20, max_value=200))),  # product_price
                                       repr(str(fake.pydecimal(right_digits=4, min_value=20, max_value=200))),  # product_amount
                                       repr(str(fake.date_between(start_date=datetime.date.fromisoformat("2000-01-01"),
                                                                  end_date=datetime.date.fromisoformat("2021-12-01")))),
                                       "gen_random_uuid()"  # id
                                       ),
                    "\n",
                ])))


if __name__ == '__main__':
    # test()
    generate()
