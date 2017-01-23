# -*- coding: utf-8 -*-

import aqt
import sys, traceback
import cgi

from anki.lang import _
from aqt.qt import *
from aqt.utils import showText, showWarning

class ErrorHandler(aqt.errors.ErrorHandler):
    customErrorHandler = True

    def __init__(self, mw):
        import aqt.errors
        aqt.errors.ErrorHandler.__init__(self, mw)
        self.errors = []
        
    def write(self, data):
        if "IOError: [Errno 2" not in data:
            # dump to stdout
            sys.stdout.write(data)
            # save in buffer
            self.pool += data
            self.errors.append(data)
            # and update timer
            self.setTimer()
