import pandas as pd
import datetime, time, uuid
from sqlalchemy import create_engine
from pandas import DataFrame

engine = create_engine('mysql+pymysql://admin:***REMOVED***@192.168.168.140:3306/erp_local')

startTime = datetime.datetime.now()

def read_original_excel(
        df: DataFrame,
        sheet_name: str,
        column_mapping: dict,
        table_name: str
):
    df = pd.read_excel(f, sheet_name)
    df.rename(columns=column_mapping, inplace=True)
    df["file_id"] = uuid.uuid4()
    df.to_sql(table_name, engine, if_exists="append")

with pd.ExcelFile(path_or_buffer="demo.xlsx") as f:
    df1 = pd.read_excel(f, "man")
    df1.rename(columns={"姓名": "name", "年龄": "age", "性别": "gender", "地址": "address"}, inplace=True)
    df1["file_id"] = uuid.uuid4()
    df1.to_sql('ent_datacenter_original_man', engine, if_exists="append")
    read_original_excel()

    df2 = pd.read_excel(f, "woman")
    df2.rename(columns={"姓名": "name", "年龄": "age", "性别": "gender", "地址": "address"}, inplace=True)
    df2["file_id"] = uuid.uuid4()
    df2.to_sql('ent_datacenter_original_woman', engine, if_exists="append")
    print("读取指定行的数据：\n{0}".format(f))


endtime = datetime.datetime.now()

seconds = (endtime - startTime).seconds
print(seconds)
