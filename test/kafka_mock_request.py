#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests


def publish(max):
    for i in range(0, max):
        r = requests.post(url="http://localhost:8000/api/data-center/match/fromInstitutionMatch",
                          data=json.dumps({
                              "inspectSaleDTO": {
                                  "id": "e2cfe615-bc64-11eb-aac7-00163e1e0729",
                                  "fromInstitutionName": "全部紫阳县红椿大药房" + str(i + 1),
                                  "fromInstitutionRinseStatus": "FAIL",
                                  "createTime": "2020-12-31 11:13:19",
                                  "updateTime": "2021-05-20 21:01:46",
                                  "businessType": "SD",
                                  "periodName": "2021财年-05",
                                  "periodId": "8ac2749979651454017968aa75480008",
                              },
                              "institutionDTO": {
                                  "score": 0.648,
                                  "address": {
                                      "0": "金盏乡黎各庄村128号"
                                  },
                                  "province": "北京市",
                                  "city": "北京市",
                                  "county": "朝阳区",
                                  "name": "北京京勇安康大药房有限公司",
                                  "standardCode": "",
                                  "alias": "",
                                  "uniqueId": "",
                                  "category": "",
                                  "state": "Active",
                                  "code": "JXS782"
                              },
                              "tabName": "enterprise",
                              "dataTypeDesc": "MONTH"
                          }),
                          headers={
                              'Content-Type': 'application/json',
                              'RS-Header-TenantId': '08dea516d0244bdaaa3a723bbe9cbd57'
                          })
        print(i + 1, "次")


if __name__ == '__main__':
    publish(200000)
