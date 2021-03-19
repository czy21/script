import profile

import pandas as pd
import datetime, time, uuid, config
from sqlalchemy import create_engine
from pymongo import MongoClient

engine = create_engine(config.MYSQL_HOST)
mongoClient = MongoClient(host=config.MONGO_HOST)

startTime = datetime.datetime.now()


def validate_null(cell):
    print(cell)


def validate(series, sd_mapping_dict):
    error_msgs = []
    if pd.isna(series["to_institution_address"]):
        error_msgs.append("客户地址为空")
    if pd.isna(series["remark"]):
        error_msgs.append("无备注")
    return ",".join(error_msgs)


with pd.ExcelFile(path_or_buffer="demo.xlsx") as f:
    table = mongoClient["spi_local"]["ent_file_column_mapping"]
    sd_mapping_list = table.find_one({"businessType": "SD"})["fields"]
    sd_mapping_dict = {}
    for t in sd_mapping_list:
        sd_mapping_dict["*" + t["header"] if "required" in t and t["required"] else t["header"]] = t["column"]
    df = pd.read_excel(f, "SD", usecols=lambda x: x in sd_mapping_dict.keys())
    df.rename(columns=sd_mapping_dict, inplace=True)
    df["file_id"] = uuid.uuid4()
    df["error"] = df.apply(lambda x: validate(x, sd_mapping_list), axis=1)
    df.to_sql("ent_sfl_inspect_sale", engine, if_exists="append")

endtime = datetime.datetime.now()

seconds = (endtime - startTime).seconds
print(seconds)
