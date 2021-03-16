import profile

import pandas as pd
import datetime, time, uuid
from sqlalchemy import create_engine
from pymongo import MongoClient

engine = create_engine('mysql+pymysql://admin:Czy.190815@192.168.2.11:3306/erp_local')
mongoClient = MongoClient(host="mongodb://admin:Czy.190815@192.168.2.11:27017/")

startTime = datetime.datetime.now()

with pd.ExcelFile(path_or_buffer="test_inspect.xlsx") as f:
    table = mongoClient["erp"]["ent_file_column_mapping"]
    sd_mapping_list = table.find_one({"businessType": "SD"})["fields"]
    sd_mapping_dict = dict(map(lambda x: (x.get('header'), x.get('column')), sd_mapping_list))

    df = pd.read_excel(f, "SD")
    df.rename(columns=sd_mapping_dict, inplace=True)
    df["file_id"] = uuid.uuid4()
    df.to_sql("ent_sfl_inspect_sale", engine, if_exists="append")

endtime = datetime.datetime.now()

seconds = (endtime - startTime).seconds
print(seconds)
