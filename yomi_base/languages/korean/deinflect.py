# -*- coding: utf-8 -*-

# needed to import javascript
from . import execjs
import os
os.environ["EXECJS_RUNTIME"] = 'PyV8'
#
# Deinflector
#

class Deinflector:
    def __init__(self,path):
        try:
            self.javascript = execjs.compile(open(path).read())
        except:
            self.pyv8 = False
        else:
            self.pyv8 = True
        
    def deinflect(self, term, validator):
        results = list()
        jsQuery = u"stemmer.stem('{0}')".format(term)
        results.append({'source': term, 'rules': list()})
        if self.pyv8:
            try:
                jsResult = self.javascript.eval(jsQuery)
                if jsResult is not None:
                    results.append({'source': jsResult, 'rules':list()})
            except Exception as e:
                print(str(e))
        return results
