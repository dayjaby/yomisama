# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/updates.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogUpdates(object):
    def setupUi(self, DialogUpdates):
        DialogUpdates.setObjectName("DialogUpdates")
        DialogUpdates.resize(500, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogUpdates)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelUpdates = QtWidgets.QLabel(DialogUpdates)
        self.labelUpdates.setWordWrap(True)
        self.labelUpdates.setOpenExternalLinks(True)
        self.labelUpdates.setObjectName("labelUpdates")
        self.verticalLayout.addWidget(self.labelUpdates)
        self.textBrowser = QtWidgets.QTextBrowser(DialogUpdates)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogUpdates)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogUpdates)
        self.buttonBox.accepted.connect(DialogUpdates.accept)
        self.buttonBox.rejected.connect(DialogUpdates.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogUpdates)

    def retranslateUi(self, DialogUpdates):
        _translate = QtCore.QCoreApplication.translate
        DialogUpdates.setWindowTitle(_translate("DialogUpdates", "Update Checker"))
        self.labelUpdates.setText(_translate("DialogUpdates", "<p>A new version of Yomichan is available for download!</p>\n"
"\n"
"<p>You can download this update (version {0} to version {1}) from the add-ons section on <a href=\"https://ankiweb.net/shared/info/934748696\">Anki Online</a> or directly from the <a href=\"http://foosoft.net/projects/yomichan\">Yomichan homepage</a>.</p>\n"
"\n"
"<p>Changes from your version are listed below:</p>"))
