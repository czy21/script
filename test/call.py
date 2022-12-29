import json
import pathlib
import pandas

if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent.joinpath("___temp/call_out.json")) as f:
        data = json.load(f)
        df = pandas.DataFrame(data=data,columns=["customer_id", "project_user_id", "back_count", "back_time"])
        df.to_excel(pathlib.Path(__file__).parent.joinpath("___temp/call_out.xlsx"), index=False)
        print(len(data))
