import multiprocessing
from datetime import datetime
from multiprocessing import Pool

import requests


def get_session(sid):
    r = requests.post(url="http://127.0.0.1:37001/api/sms/batchSend",
                      headers={
                          "authorization": "b530c5984da54f398552f7241da6eb17"
                      },
                      json={
                          "phoneNumbers": [
                              "15145033859"
                          ],
                          "businessType": "CUSTOMER_SERVICE"
                      })
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
