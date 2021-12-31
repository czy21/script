from datetime import datetime
from multiprocessing import Pool

import requests


def get_session(sid):
    r = requests.post(url="http://127.0.0.1:8080/user/search".format(sid), headers={})
    print(r.json())


if __name__ == '__main__':

    start_time = datetime.now()

    p = Pool(20)
    for f in range(0, 1000):
        p.apply_async(get_session, args=(str(f + 1),))
    p.close()
    p.join()
    end_time = datetime.now()
    seconds = (end_time - start_time).seconds
    print("总耗时: ", seconds)
