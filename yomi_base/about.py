# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import constants
import gen.about_ui


class DialogAbout(QtGui.QDialog, gen.about_ui.Ui_DialogAbout):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        text = unicode(self.labelVersion.text())
        text = text.format(constants.c['appVersion'])
        self.labelVersion.setText(text)
