#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore
from .yomi_base.reader import MainWindowReader
from .yomi_base.yomichan import Yomichan
from .yomi_base.file_state import FileState
import sys


class YomichanStandalone(Yomichan):
    def __init__(self):
        Yomichan.__init__(self)

        self.application = QtGui.QApplication(sys.argv)
        self.window = MainWindowReader(
            self,
            None,
            self.preferences,
            self.language,
            filename=sys.argv[1] if len(sys.argv) >= 2 else None
        )

        self.window.show()
        self.application.exec_()


if __name__ == '__main__':
    yomichanInstance = YomichanStandalone()
else:
    from .yomi_base.anki_bridge import yomichanInstance
