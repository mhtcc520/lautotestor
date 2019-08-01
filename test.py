#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 19:31:52 2019

@author: haitao
"""

import base

case = base.case("./suits/tag/general.json")
case.run()
case.show_report()
#url = "http://192.168.16.127:4922/api/embed/tag/v1/add"
#url = "http://192.168.16.127:4922/"
#headers = {'content-type': 'application/json','accept': 'application/json'}
#body = {"desc": "mqtt module","egid": 2, "name": "mqtt","owner": "maht@tuya.com","type": 1, "uid": "0123456789"}
##body = "{\n \"desc\": \"mqtt module\", \n \"egid\": 2, \n \"name\": \"mqtt\",\n \"owner\": \"maht@tuya.com\",\n \"type\": 1, \"uid\": \"0123456789\"}"
#r = requests.post(geturl("api/embed/tag/v1/add"), json2str(body), headers)
#print(r.json())
#print(r.json()['success'])

#print(getname("c:/windows/system32"))



