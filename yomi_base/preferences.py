# -*- coding: utf-8 -*-

from PyQt6 import QtWidgets, QtCore, QtGui
import copy
from .gen import preferences
import locale

locale.setlocale(locale.LC_ALL, '')
        
lookupKeys = [
            ('Insert',QtCore.Qt.Key.Key_Insert),
            ('Shift',QtCore.Qt.Key.Key_Shift),
            ('Pause',QtCore.Qt.Key.Key_Pause),
            ('F1',QtCore.Qt.Key.Key_F1)
        ]

class DialogPreferences(QtWidgets.QDialog, preferences.Ui_DialogPreferences):
    def __init__(self, parent, preferences, anki, profiles):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.preferences = preferences
        self.anki = anki

        self.accepted.connect(self.onAccept)
        self.buttonColorBg.clicked.connect(self.onButtonColorBgClicked)
        self.buttonColorFg.clicked.connect(self.onButtonColorFgClicked)
        self.comboBoxDeck.currentIndexChanged.connect(self.onDeckChanged)
        self.comboBoxModel.currentIndexChanged.connect(self.onModelChanged)
        self.comboFontFamily.currentFontChanged.connect(self.onFontFamilyChanged)
            
        self.spinFontSize.valueChanged.connect(self.onFontSizeChanged)
        self.tableFields.itemChanged.connect(self.onFieldsChanged)       
        idx = 0
        for name, key in lookupKeys:
            self.comboBoxLookupKey.insertItem(idx,name,key)
            idx = idx+1

        self.profileObjs = profiles
        for profile in profiles.values():
            profile.onShowDialogPreferences(self)
        self.dataToDialog()
        for profile in profiles.values():
            profile.radioButton.toggled.connect(self.onProfileChanged)


    def dataToDialog(self):
        self.checkCheckForUpdates.setChecked(self.preferences['checkForUpdates'])
        self.checkRememberTextContent.setChecked(self.preferences['rememberTextContent'])
        self.checkAllowEditing.setChecked(self.preferences['allowEditing'])
        self.checkLoadRecentFile.setChecked(self.preferences['loadRecentFile'])
        self.checkStripReadings.setChecked(self.preferences['stripReadings'])
        self.spinMaxResults.setValue(self.preferences['maxResults'])
        self.spinScanLength.setValue(self.preferences['scanLength'])
        self.checkUnlockVocab.setChecked(self.preferences['unlockVocab'])
        if self.checkHideTranslation is not None:
            self.checkHideTranslation.setChecked(self.preferences['hideTranslation'])
        self.comboBoxLookupKey.setCurrentIndex(self.preferences['lookupKey'])
        self.updateSampleText()
        font = self.textSample.font()
        self.comboFontFamily.setCurrentFont(font)
        self.spinFontSize.setValue(font.pointSize())

        if self.anki is not None:
            self.tabAnki.setEnabled(True)
            self.profiles = copy.deepcopy(self.preferences['profiles'])
            self.profileToDialog()


    def dialogToData(self):
        self.preferences['checkForUpdates'] = self.checkCheckForUpdates.isChecked()
        self.preferences['rememberTextContent'] = self.checkRememberTextContent.isChecked()
        self.preferences['allowEditing'] = self.checkAllowEditing.isChecked()
        self.preferences['loadRecentFile'] = self.checkLoadRecentFile.isChecked()
        self.preferences['maxResults'] = self.spinMaxResults.value()
        self.preferences['scanLength'] = self.spinScanLength.value()
        self.preferences['unlockVocab'] = self.checkUnlockVocab.isChecked()
        if self.checkHideTranslation is not None:
            self.preferences['hideTranslation'] = self.checkHideTranslation.isChecked()
        self.preferences['stripReadings'] = self.checkStripReadings.isChecked()
        self.preferences['lookupKey'] = self.comboBoxLookupKey.currentIndex()
        self.preferences['firstRun'] = False

        if self.anki is not None:
            self.dialogToProfile()
            self.preferences['profiles'] = self.profiles


    def dialogToProfile(self):
        self.setActiveProfile({
            'deck': self.comboBoxDeck.currentText(),
            'model': self.comboBoxModel.currentText(),
            'fields': self.ankiFields()
        })


    def profileToDialog(self):
        profile, name = self.activeProfile()

        deck = str() if profile is None else profile['deck']
        model = str() if profile is None else profile['model']

        self.comboBoxDeck.blockSignals(True)
        self.comboBoxDeck.clear()
        deckNames = sorted(self.anki.deckNames())
        self.comboBoxDeck.addItems(deckNames)
        self.comboBoxDeck.setCurrentIndex(self.comboBoxDeck.findText(deck))
        self.comboBoxDeck.blockSignals(False)

        self.comboBoxModel.blockSignals(True)
        self.comboBoxModel.clear()
        modelNames = sorted(self.anki.modelNames())
        self.comboBoxModel.addItems(modelNames)
        self.comboBoxModel.setCurrentIndex(self.comboBoxModel.findText(model))
        self.comboBoxModel.blockSignals(False)

        allowedTags = self.profileObjs[name].allowedTags

        allowedTags = map(lambda t: '<strong>{' + t + '}<strong>', allowedTags)
        self.labelTags.setText('Allowed tags are {0}'.format(', '.join(allowedTags)))

        self.updateAnkiFields()


    def updateSampleText(self):
        palette = self.textSample.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(*self.preferences['bgColor']))
        palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor(*self.preferences['fgColor']))
        self.textSample.setPalette(palette)

        font = self.textSample.font()
        font.setFamily(self.preferences['fontFamily'])
        font.setPointSize(self.preferences['fontSize'])
        self.textSample.setFont(font)


    def setAnkiFields(self, fields, fieldsPrefs):
        if fields is None:
            fields = list()

        self.tableFields.blockSignals(True)
        self.tableFields.setRowCount(len(fields))

        for i, name in enumerate(fields):
            columns = list()

            itemName = QtWidgets.QTableWidgetItem(name)
            itemName.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable)
            columns.append(itemName)

            itemValue = QtWidgets.QTableWidgetItem(fieldsPrefs.get(name, ""))
            columns.append(itemValue)

            for j, column in enumerate(columns):
                self.tableFields.setItem(i, j, column)

        self.tableFields.blockSignals(False)


    def ankiFields(self):
        result = dict()

        for i in range(0, self.tableFields.rowCount()):
            itemName = self.tableFields.item(i, 0).text()
            itemValue = self.tableFields.item(i, 1).text()
            result[itemName] = itemValue

        return result


    def onAccept(self):
        self.dialogToData()


    def onButtonColorFgClicked(self):
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(*self.preferences['fgColor']), self)
        if color.isValid():
            self.preferences['fgColor'] = [color.red(), color.green(), color.blue(), color.alpha()]
            self.updateSampleText()


    def onButtonColorBgClicked(self):
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(*self.preferences['bgColor']), self)
        if color.isValid():
            self.preferences['bgColor'] = [color.red(), color.green(), color.blue(), color.alpha()]
            self.updateSampleText()


    def onFontFamilyChanged(self, font):
        self.preferences['fontFamily'] = font.family()
        self.updateSampleText()


    def onFontSizeChanged(self, size):
        self.preferences['fontSize'] = size
        self.updateSampleText()


    def onModelChanged(self, index):
        self.updateAnkiFields()
        self.dialogToProfile()


    def onDeckChanged(self, index):
        self.dialogToProfile()


    def onFieldsChanged(self, item):
        self.dialogToProfile()
        

    def onProfileChanged(self, data):
        self.profileToDialog()


    def updateAnkiFields(self):
        modelName = self.comboBoxModel.currentText()
        fieldNames = self.anki.modelFieldNames(modelName) or list()

        profile, name = self.activeProfile()
        fields = dict() if profile is None else profile['fields']

        self.setAnkiFields(fieldNames, fields)


    def activeProfile(self):
        for profile in self.profileObjs.values():
            if profile.radioButton.isChecked():
                return self.profiles.get(profile.name), profile.name

    def setActiveProfile(self, p):
        for profile in self.profileObjs.values():
            if profile.radioButton.isChecked():
                self.profiles[profile.name] = p
