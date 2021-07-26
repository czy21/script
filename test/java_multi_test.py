import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests


def detail(x):
    r = requests.post(url="http://192.168.2.21:8076/user/detail",
                      data=json.dumps({
                          "id": "2f5aa878-352d-49a9-a18e-188449e9e649"
                      }),
                      headers={
                          'Content-Type': 'application/json'
                      })
    ret = " ".join([
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        str(x),
        str(r.json()),
        str(time.time())
    ])
    print(ret)
    return ret


if __name__ == '__main__':
    print('MainThread %s is running...' % threading.current_thread().name)
    result = []
    with ThreadPoolExecutor(16) as executor:
        for data in executor.map(detail, range(10000)):
            result.append(data)
    print(result)
    print('MainThread %s ended.' % threading.current_thread().name)
