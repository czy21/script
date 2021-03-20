import numpy as np
from cerberus import errors, Validator

import config
import uuid
from datetime import datetime

import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine

engine = create_engine(config.MYSQL_HOST)
mongoClient = MongoClient(host=config.MONGO_HOST)

startTime = datetime.now()
print("start time:", startTime)


# class Cell():
#
#     def integer(self, value):
#         return isinstance(value, int)
#
#     def float(self, value):
#         return isinstance(value, float)
#
#     def date(self, value):
#         return isinstance(value, datetime)


def validate(series, mapping_list: list):
    error_msgs = []

    for t in mapping_list:
        for s in t.get("validators", []):
            message = s.pop('message')

            class CustomErrorHandler(errors.BasicErrorHandler):
                messages = errors.BasicErrorHandler.messages.copy()
                messages[errors.REQUIRED_FIELD.code] = message
                messages[errors.BAD_TYPE.code] = message

            schema = {t["header"]: s}
            v = Validator(schema, error_handler=CustomErrorHandler)
            v.validate({t["header"]: series.get(t["header"])}, schema)

            print(v.errors)
        # arr = t.get("validators", [])
        # required = list(filter(lambda c: c.get("required", False), arr))
        # cell_value = series.get(t.get("header"))
        # validate = required and pd.isna(cell_value)
        # if :
        #     error_msgs.append(",".join(list(map(lambda f: f["message"], required))))
        #     break

        # print("ss")
        # for v in t.get("validators", []):
        #     if v.get("required", False) and "*" + t.get("header") in series and pd.isna(series.get("*" + t.get("header"))):
        #         error_msgs.append(v["message"])
        #         break
        #     if v.get("type") == "date" and not isinstance(series.get("*" + t["column"] if v.get("required", False) else t["column"]), datetime):
        #         error_msgs.append(v["message"])

    return ",".join(error_msgs) if error_msgs else None


with pd.ExcelFile(path_or_buffer="1K.xlsx") as f:
    table = mongoClient["spi_local"]["ent_file_column_mapping"]
    sd_mapping_list = []
    for m in table.find_one({"businessType": "SD"})["fields"]:
        for v in m.get("validators", []):
            message = v.pop("message")
            schema = v
            v.clear()
            v = dict({"schema": schema, "message": message})
        sd_mapping_list.append(m)
    sd_mapping_dict = dict((t["header"], t["column"]) for t in sd_mapping_list)
    df = pd.read_excel(f, "SD")
    df["错误"] = df.apply(lambda x: validate(x, sd_mapping_list), axis=1)

    resolve_time = datetime.now()
    print("解析耗时:", (resolve_time - startTime).seconds)

    if df["错误"].isnull().all():
        except_columns = list(filter(lambda c: c not in sd_mapping_dict.keys(), df.columns))
        df.drop(columns=except_columns, inplace=True)
        df.rename(columns=sd_mapping_dict, inplace=True)
        df["file_id"] = uuid.uuid4()
        df["id"] = df.apply(lambda _: uuid.uuid4(), axis=1)
        df["row_number"] = df.apply(lambda x: (x.name + 1), axis=1)
        df.to_sql(name="ent_sfl_inspect_sale", con=engine, if_exists="replace", index=False)
    else:
        print("有错误")
        df.to_excel("error.xlsx", index=False)

endtime = datetime.now()
print("end time:", endtime)

seconds = (endtime - startTime).seconds
print("总耗时: ", seconds)
