#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 19:31:52 2019

@author: haitao
"""

import requests
import json
import os

url = "http://192.168.137.1:4922/"
headers = {'content-type': 'application/json','accept': 'application/json'}

def json2str(obj):
    str = json.dumps(obj, indent=2)
    return str

def geturl(route):
    return url+route

def getname(dir):
    path, name = os.path.split(dir)
    name = os.path.splitext(name)
    return name

def postcmd(path, body):
    #print(path, body)
    ret = requests.post(geturl(path), json2str(body), headers)
    print(ret)
    return ret.json()

def checkexpect(result, expect):
    #print(result)
    #print(expect)
    for key in expect.keys():
        if key in result.keys():
            if key == "result":            
                for i in expect[key].keys():
                    if i in result[key].keys():
                        s1=json.dumps(result[key][i], indent=2, ensure_ascii=False)
                        s2=json.dumps(expect[key][i], indent=2, ensure_ascii=False)
                        #print(s1)
                        #print(s2)
                        if s1 != s2:
                            return False           
                    else:
                        return False
            else:
                s1=json.dumps(result[key], indent=2, ensure_ascii=False)
                s2=json.dumps(expect[key], indent=2, ensure_ascii=False)
                #print(s1)
                #print(s2)
                if s1 != s2:
                    return False
        else:
            return False
    return True

def tryexec(cmd):    
    if not ("path" in cmd.keys()) and not ("body" in cmd.keys()):
        print("cmd not valid")
        return False
        
    #print("try to execute command:")
    #print(json.dumps(cmd, indent=2, ensure_ascii=False))
    
    result = postcmd(cmd["path"], cmd["body"])
    
    if "success" in result.keys() and result["success"] == False:
        print("try to execute command but failed:")
        print(json.dumps(cmd, indent=2, ensure_ascii=False))
    
    
    print("execute command got result:")
    #print(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if "expect" in cmd.keys():
        ret = checkexpect(result, cmd["expect"])
        if ret:
            return True, result
        else:        
            print("result is not expected:")
            print(json.dumps(cmd["expect"], indent=2, ensure_ascii=False))
            return False,result
    else:
        return result['success'], result
    
    

