# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from .. import reader_util

try:
    fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def fromUtf8(s):
        return s

try:
    encoding = QtWidgets.QApplication.UnicodeUTF8
    def translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, encoding)
except AttributeError:
    def translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class GenericProfile:
    name = ""
    displayedName = ""
    descriptor = ""
    allowedTags = []
    languages = []
    sortIndex = 0
    instance = None

    def __init__(self,reader):
        self.definitions = []
        self.existsAlready = {}
        self.reader = reader
        self.textField = None
        self.html = ""
        self.defBody = ""
        self.__class__.instance = self

    def addFact(self,definition):
        self.reader.ankiAddFact(self.name,self.markup(definition))

    def overwriteFact(self,definition):
        self.reader.ankiOverwriteFact(self.name,self.markup(definition))

    def onLookup(self,content,lengthMatched):
        return lengthMatched

    def onShowDialogPreferences(self,dialog):
        self.radioButton = QtWidgets.QRadioButton(dialog.tabAnki)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName(fromUtf8("radioButton" + self.displayedName))
        dialog.horizontalLayout_2.addWidget(self.radioButton)
        self.radioButton.setText(translate("DialogPreferences", self.displayedName, None))
        return

    def getFileProfile(self,prfl):
        return self.reader.currentFile.profiles[prfl]

    def ankiIsFactValid(self, prfl, markup, index=None):
        if markup is None:
            return False

        if self.reader.anki is None:
            return False

        profile = self.reader.preferences['profiles'].get(prfl)
        if profile is None:
            return False
        fields = reader_util.formatFields(profile['fields'], markup)
        key = self.reader.anki.getModelKey(profile['model'])
        fp = self.getFileProfile(prfl)
        if fp['longestMatch'] is None:
            fp['longestMatch'] = index
        if key is not None and key in fields and fields[key] in fp['wordsAll']:
            if len(fields[key]) > len(fp['longestMatchKey']):
                fp['longestMatch'] = index
                fp['longestMatchKey'] = fields[key]
        result = self.reader.anki.canAddNote(profile['deck'], profile['model'], fields)

        return result

    def updateDefinitions(self,**options):
        self.existsAlready = {}
        defs = self.definitions[:]
        if options.get('trim', True):
            defs = defs[:self.reader.preferences['maxResults']]
        html = self.buildDefinitions(defs,self.reader.anki is not None)
        html = self.fixHtml(html)
        control = self.textField

        # TODO: Fix this
        ## position = control.page().mainFrame().scrollBarValue(QtCore.Qt.Vertical)
        self.textField.setHtml(html)

        ## if options.get('scroll', False):
        ##    control.page().mainFrame().setScrollBarValue(QtCore.Qt.Vertical,position)

    def fixHtml(self,html):
        return html

    def buildDefHeader(self):
        palette = QtWidgets.QApplication.palette()
        toolTipBg = palette.color(QtGui.QPalette.Window).name()
        toolTipFg = palette.color(QtGui.QPalette.WindowText).name()

        return u"""
            <html><head><style>
            body {{ background-color: {0}; color: {1}; font-size: 11pt; font-family:Arial; }}
            span.expression {{ font-size: 15pt; font-family:Arial; }}
            span.expression a {{ text-decoration: none; }}
            span.german {{ font-size: 18pt; font-family:Arial; }}
            span.online {{ font-size: 15pt; font-family:Arial; }}
            span.online ol {{ list-style-type: none; }}
            </style></head><body>""".format(toolTipBg, toolTipFg)

    def buildDefFooter(self):
        return '</body></html>'

    def buildDefBody(self, definition, index, allowOverwrite):
        return ''

    def buildEmpty(self):
        return u"""<p>No definitions to display.</p>"""

    def buildDefinitions(self, definitions, allowOverwrite):
        self.defBody = ""
        self.html = self.buildDefHeader()

        if len(definitions) > 0:
            for i, definition in enumerate(definitions):
               self.defBody += self.buildDefBody(definition, i, allowOverwrite)
            self.html += self.defBody
        else:
            self.html += self.buildEmpty()

        self.html = self.html + self.buildDefFooter()
        return self.html

    def afterFileLoaded(self):
        pass

    def close(self):
        pass
