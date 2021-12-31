from datetime import datetime
from multiprocessing import Pool

import requests


def get_session(sid):
    r = requests.post(url="http://192.168.2.21:48926/user/search".format(sid), headers={})
    print(r.content)


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
