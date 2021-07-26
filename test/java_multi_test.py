import datetime
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
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    current_timestamp = str(time.time())
    current_user = str(x + 1)
    response_data = r.json()
    map = {
        "current_user": current_user,
        "current_time": current_time,
        "response_data": response_data,
        "current_timestamp": current_timestamp
    }
    return map


def user_update(x):
    start_time = datetime.datetime.now()
    r = requests.post(url="http://127.0.0.1:8080/stock/sale",
                      data=json.dumps({
                          "id": "2f5aa878-352d-49a9-a18e-188449e9e649"
                      }),
                      headers={
                          'Content-Type': 'application/json'
                      })
    end_time = datetime.datetime.now()
    current_user = str(x + 1)
    request_time = str((end_time - start_time).microseconds / 1000) + "ms"
    response_data = r.json()
    map = {
        "user": current_user,
        "request_time": request_time,
        "response_data": response_data
    }
    return map


if __name__ == '__main__':
    print('MainThread %s is running...' % threading.current_thread().name)
    result = []
    with ThreadPoolExecutor(16) as executor:
        for data in executor.map(user_update, range(10)):
            result.append(data)
    for t in result:
        print(t)
    print('MainThread %s ended.' % threading.current_thread().name)
