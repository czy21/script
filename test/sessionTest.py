from datetime import datetime
from multiprocessing import Pool

import requests


def get_session(sid):
    r = requests.get(url="http://127.0.0.1:8080/session/test2?sid={0}".format(sid), headers={"Cookie": "sid=" + sid})
    print(r.content)


if __name__ == '__main__':

    start_time = datetime.now()

    p = Pool(20)
    for f in range(0, 50):
        p.apply_async(get_session, args=(str(f + 1),))
    p.close()
    p.join()
    end_time = datetime.now()
    seconds = (end_time - start_time).seconds
    print("总耗时: ", seconds)
