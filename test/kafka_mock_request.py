#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests


def publish(max):
    for i in range(0, max):
        r = requests.post(url="http://127.0.0.1:8080/user/publicMsg",
                          data=json.dumps({
                              "topic": "my-topic",
                              'msg': "国药控股云南有限公司,广西九州通医疗器械有限公司,上海软素经销商,哈尔滨凯德医院,哈尔滨仁圣医院,黑龙江省肿瘤医院,黑龙江大学医院,哈尔滨口岸医院,哈尔滨仁爱医院,黑龙江省第二医院,黑龙江省医院,哈尔滨建国医院,黑龙江公明医院,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583,华润广西医药有限公司55583"
                          }),
                          headers={'Content-Type': 'application/json'})
        print(i, "次")


if __name__ == '__main__':
    publish(3000)
