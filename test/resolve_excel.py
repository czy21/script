import profile

import numpy as np
import pandas as pd
import datetime, time, uuid, config
from sqlalchemy import create_engine
from pymongo import MongoClient

engine = create_engine(config.MYSQL_HOST)
mongoClient = MongoClient(host=config.MONGO_HOST)

startTime = datetime.datetime.now()
print("start time:", startTime)


def validate_null(cell):
    print(cell)


def validate(series, mapping_list: list):
    error_msgs = []
    for t in mapping_list:
        for v in t.get("validators", []):
            if v.get("required", False) and t.get("column") in series and pd.isna(series.get(t["column"])):
                error_msgs.append(v["message"])

    return ",".join(error_msgs) if error_msgs else None


with pd.ExcelFile(path_or_buffer="100W.xlsx") as f:
    table = mongoClient["spi_local"]["ent_file_column_mapping"]
    sd_mapping_list = table.find_one({"businessType": "SD"})["fields"]
    sd_mapping_dict = {}
    for t in sd_mapping_list:
        sd_mapping_dict["*" + t["header"] if t.get("validators") is not None and any([p.get("required") for p in t.get("validators")]) else t["header"]] = t["column"]
    df = pd.read_excel(f, "SD", usecols=lambda x: x in sd_mapping_dict.keys())
    df.rename(columns=sd_mapping_dict, inplace=True)
    df["file_id"] = uuid.uuid4()
    df["id"] = df.apply(lambda _: uuid.uuid4(), axis=1)
    df["row_number"] = df.apply(lambda x: (x.name + 1), axis=1)
    df["error"] = df.apply(lambda x: validate(x, sd_mapping_list), axis=1)

    resolve_time = datetime.datetime.now()
    print("解析耗时:", (resolve_time - startTime).seconds)

    df.to_sql("ent_sfl_inspect_sale", engine, if_exists="replace", index=False)

endtime = datetime.datetime.now()
print("end time:", endtime)

seconds = (endtime - startTime).seconds
print("总耗时: ", seconds)
