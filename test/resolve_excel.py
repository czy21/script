import pandas as pd
import datetime, time, uuid
from sqlalchemy import create_engine
from pandas import DataFrame

engine = create_engine('mysql+pymysql://admin:Czy.190815@192.168.2.4:3306/erp_local')

startTime = datetime.datetime.now()


def read_original_excel(
        df: DataFrame,
        sheet_name: str,
        column_mapping: dict,
        table_name: str
):
    df = pd.read_excel(df, sheet_name)
    df.rename(columns=column_mapping, inplace=True)
    df["file_id"] = uuid.uuid4()
    df.to_sql(table_name, engine, if_exists="append")


with pd.ExcelFile(path_or_buffer="demo.xlsx") as f:
    read_original_excel(df=f, sheet_name="man", column_mapping={"姓名": "name", "年龄": "age", "性别": "gender", "地址": "address"}, table_name="ent_sys_man")
    read_original_excel(df=f, sheet_name="woman", column_mapping={"姓名": "name", "年龄": "age", "性别": "gender", "地址": "address"}, table_name="ent_sys_woman")
    print("读取指定行的数据：\n{0}".format(f))

endtime = datetime.datetime.now()

seconds = (endtime - startTime).seconds
print(seconds)
