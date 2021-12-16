import json
from pathlib import Path

from faker import Faker

fake = Faker(locale="zh-CN")
met_file_column_mapping_path = Path(__file__).parent.joinpath("met_file_column_mapping.json")
with open(met_file_column_mapping_path.as_posix(), "r", encoding="utf-8") as mf:
    met_file_column_list = json.load(mf)
sale_mapping = next(filter(lambda t: t["tableName"] == "ent_sale", met_file_column_list))

# for t in range(0, 1):
#     print(fake.company())
#     print(fake.phone_number())
#     print(fake.name())
#     print(fake.address())
