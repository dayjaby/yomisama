# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from . import constants
from .gen import about_ui


class DialogAbout(QtWidgets.QDialog, about_ui.Ui_DialogAbout):
    def __init__(self, parent):
        QtWIdgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        text = self.labelVersion.text()
        text = text.format(constants.c['appVersion'])
        self.labelVersion.setText(text)
