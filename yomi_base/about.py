# -*- coding: utf-8 -*-

from PyQt6 import QtWidgets
from . import constants
from .gen import about


class DialogAbout(QtWidgets.QDialog, about.Ui_DialogAbout):
    def __init__(self, parent):
        QtWIdgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        text = self.labelVersion.text()
        text = text.format(constants.c['appVersion'])
        self.labelVersion.setText(text)
