import multiprocessing
from datetime import datetime
from multiprocessing import Pool

import requests


def get_session(sid):
    r = requests.get(url="http://demo-dev.czy21.com/api/demo-portal/test/lbTest")
    print(r.json())


if __name__ == '__main__':

    start_time = datetime.now()

    p = Pool(multiprocessing.cpu_count() * 2)
    for f in range(0, 10000):
        p.apply_async(get_session, args=(str(f + 1),))
    p.close()
    p.join()
    end_time = datetime.now()
    seconds = (end_time - start_time).seconds
    print("总耗时: ", seconds)
