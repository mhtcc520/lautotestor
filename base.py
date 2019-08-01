#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 19:31:52 2019

@author: haitao
"""

import os
import public
import json
import codecs

class report:
    def __init__(self, level, name):
        self.status = True
        self.level = level
        self.name = name
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errmsg = ""
        self.reports = []
        
    def addreport(self, ret, result):
        if self.level == "at":
            self.total += result.total
            self.status = False
            self.failed += result.failed
            self.passed += result.passed   
        elif self.level == "suit":
            self.total += 1
            if ret == False:
                self.status = False
                self.failed += 1
            else:
                self.passed += 1             
        else:
            self.total += 1
            if ret == False:
                self.errmsg = json.dumps(result, indent=2, ensure_ascii=False)
                self.status = False
                self.failed += 1
            else:
                self.passed += 1
            
        self.reports.append(result)
        return True              
        
    def report(self):
        print("****************************************")
        print("*autotest status: {}".format(self.status))
        print("****************************************")
        if self.level != "case":
            print("*total: {}".format(self.total))
            print("*passed: {}".format(self.passed))
            print("*failed: {}".format(self.failed))
            print("*****************result*****************")
            for r in self.reports:
                if r.level == "suit":
                    print("*suit: {}   {}".format(r.name, r.status))
                    for rc in r.reports:
                        print("*    case:  {}   {}".format(rc.name, rc.status))
                        if rc.status == False:
                            print("error message:")
                            print(rc.errmsg)
                elif r.level == "case":
                    print("*    case:  {}   {}".format(r.name, r.status))
                    if r.status == False:
                        print("error message:")
                        print(r.errmsg)
        else:
            print("*****************result*****************")
            print("*    case:  {}   {}".format(self.name, self.status))
            if self.status == False:
                print("error message:")
                print(self.errmsg)
            #for r in self.reports:
            #    print(json.dumps(r, indent=2, ensure_ascii=False))                                   
        print("******************end*******************")


class case:    
    def __init__(self, case_file_dir):
        #print(case_file_dir)
        case_file = codecs.open(case_file_dir, "a+", "utf-8")
        cfg = json.load(case_file, encoding='utf-8')
        #cfg = yaml.load(case_file, encoding='utf-8')

        self.dir = case_file_dir
        self.ctors = []
        self.steps = []
        self.teardowns = []
        self.name = json.dumps(cfg["name"])
        if "ctors" in cfg.keys():
            self.ctors = cfg["ctors"]
        if "steps" in cfg.keys():
            self.steps = cfg["steps"]
        self.report = report("case", self.name)        

    def checkrefer(self, obj):
        if "refers" in obj.keys():
            for refer in obj["refers"]:
                for ctor in self.ctors:
                    #print(ctor["name"])
                    #print(refer["name"])
                    if ctor["name"] == refer["name"]:
                        #print("xxxxxxxxxxxxxxxxxxxxxx")
                        #print(obj)
                        #print("yyyyyyyyyyyyyyyyyyyyyy")
                        #print(ctor["result"])
                        if "translate" in refer.keys():
                            if refer["d"] in ctor["result"]["result"].keys():
                                obj["body"][refer["s"]]+=json.dumps(ctor["result"]["result"][refer["d"]])
                                if "mode" in refer.keys():
                                    if refer["mode"] == "append":
                                        obj["body"][refer["s"]]+=";"
                        else:
                            if refer["d"] in ctor["result"]["result"].keys():
                                obj["body"][refer["s"]]=ctor["result"]["result"][refer["d"]]
                        break
                        
                for step in self.steps:
                    if step["name"] == refer["name"]:
                        #print("xxxxxxxxxxxxxxxxxxxxxx")
                        #print(obj)
                        #print("yyyyyyyyyyyyyyyyyyyyyy")
                        #print(step["result"])
                        if "translate" in refer.keys():
                            if refer["translate"] == "tostring":
                                if refer["d"] in step["result"]["result"].keys():
                                    obj["body"][refer["s"]]+=json.dumps(step["result"]["result"][refer["d"]])
                                    if "mode" in refer.keys():
                                        if refer["mode"] == "append":
                                            obj["body"][refer["s"]]+=";"
                        else:
                            if refer["d"] in step["result"]["result"].keys():
                                obj["body"][refer["s"]]=step["result"]["result"][refer["d"]]
                        break
                        
        return True
    
    def runctors(self):
        for ctor in self.ctors:
            print(ctor["description"])
            self.checkrefer(ctor)
            
            ret, result = public.tryexec(ctor)
            self.report.addreport(ret, result)
            ctor["result"] = result
            if ret == False:
                return ret
            else:
                if "teardown" in ctor.keys():            
                    teardown = ctor["teardown"]
                    teardown["result"] = result
                    self.teardowns.append(teardown)                    
                    #print(ctor)
        return True
            
    def runsteps(self):
        for step in self.steps:
            print(step["description"])
            self.checkrefer(step)
                
            ret, result = public.tryexec(step)
            step["result"] = result                
            self.report.addreport(ret, result)
            if ret == False:
                return ret
            else:
                if "teardown" in step.keys():            
                    teardown = step["teardown"]
                    teardown["result"] = result
                    self.teardowns.append(teardown)     

        return True      
        
    def runteardowns(self):
        self.teardowns.reverse()
        
        #stepsa
        for teardown in self.teardowns:
            print(teardown["description"])
            if "result" in teardown.keys():
                if teardown["result"]["success"] == True:
                    for key in teardown["body"]:
                        if key in teardown["result"]["result"].keys():
                            teardown["body"][key] = teardown["result"]["result"][key]    
                    
                    public.tryexec(teardown)
                    
        return True
        
    def run(self):
        print("start run case ", self.name, " ctors")
        ret = self.runctors()
        #print(ret)
        if ret == False:
            self.runteardowns()
            return False, self.report
        
        print("start run case ", self.name, " steps")
        ret = self.runsteps()
        #print(ret)
        if ret == False:
            self.runteardowns()
            return False, self.report   
        
        print("start run case ", self.name, " teardowns")
        ret = self.runteardowns()
        if ret == False:
            return False, self.report   
                
        return True, self.report
    
    def show_report(self):
        self.report.report()

class suit:
    total_cases = 0
    
    def __init__(self, suit_dir):
        self.dir = suit_dir
        self.name = public.getname(suit_dir)
        self.report = report("suit", self.name)
        self.cases = []
        
        #load cases
        self.loadcases()
        
    def loadcases(self):
        files = os.listdir(self.dir)
        for f in files:
            name, ext = os.path.splitext(f)
            #print(name, ext)
            if ext == ".json":              
                self.total_cases += 1
                c = case(self.dir+"/"+f)
                self.cases.append(c)
        return True
    
    def runcases(self):
        for case in self.cases:
            ret, result = case.run()
            self.report.addreport(ret, result)
            #if ret == False:
            #    return ret, self.report      
        
        return True, self.report
    
    def run(self):
        self.runcases()
        return self.report.status, self.report
    
    def show_report(self):
        self.report.report()
        

                