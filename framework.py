#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 19:31:52 2019

@author: haitao
"""
import base
import os

suit_path = './suits/'

class CIAutoteser:
    
    def __init__(self):
        self.status = "not run"
        self.suits = []
        self.report = base.report("at", "autotester")
        
        #load suits
        dirs = os.listdir(suit_path)
        for name in dirs:
            name = os.path.join(suit_path, name)
            if os.path.isdir(name):
                s = base.suit(name)
                self.suits.append(s)
                
        
    def run(self):
        for suit in self.suits:
            ret, report = suit.run()
            self.report.addreport(ret, report)
            
    def show_report(self):
            self.report.report()
            return True
            
if __name__ == '__main__':
    #run all test cases
    at = CIAutoteser();
    at.run();
    at.show_report();
    
    #run suits
    #suit = base.suit("./suits/tag")
    #suit.run()
    #suit.show_report()
    
    #run case
    #case = base.case("./suits/group/list.json")
    #case.run()
    #case.show_report()
    