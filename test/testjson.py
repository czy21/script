import json

import requests


def test1():
    a = "[{\"insureID\":\"111\",\"userBirth\":\"2011-01-01\",\"userSex\":1}]"
    b = json.loads(a)
    c = json.dumps(b)
    e = [
        {
            "a": 1,
            "b": 2
        }
    ]


def test2():
    r = requests.get(url="http://demo-dev.cluster.com/api/demo-portal/test/lbTest")


if __name__ == '__main__':
    print("a")
