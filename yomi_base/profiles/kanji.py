from aqt.webview import AnkiWebView
from PyQt4 import QtGui
from profile import *

class KanjiProfile(GenericProfile):
    name = "kanji"
    descriptor = "KANJI IN THIS TEXT"
    displayedName = "Kanji"
    languages = ["japanese"]
    sortIndex = 2
    allowedTags = ['character', 'onyomi', 'kunyomi', 'glossary']

    def __init__(self,reader):
        GenericProfile.__init__(self,reader)
        
        self.dockKanji = QtGui.QDockWidget(reader)
        self.dockKanji.setObjectName(fromUtf8("dockKanji"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(fromUtf8("verticalLayout"))
        self.textField = AnkiWebView()
        self.textField.setAcceptDrops(False)
        self.textField.setObjectName("textField")
        self.verticalLayout.addWidget(self.textField)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(fromUtf8("horizontalLayout_3"))
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.dockKanji.setWidget(self.dockWidgetContents)
        reader.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockKanji)
        self.dockKanji.visibilityChanged.connect(self.onVisibilityChanged)
        self.dockKanji.setWindowTitle(translate("MainWindowReader", "Kanji", None))
        self.textField.setLinkHandler(self.onAnchorClicked)


        # menu entries to toggle visibility of the Kanji dock
        self.actionToggleKanji = QtGui.QAction(reader)
        self.actionToggleKanji.setCheckable(True)
        self.actionToggleKanji.setObjectName("actionToggleKanji")
        self.actionToggleKanji.setText("&Kanji")
        self.actionToggleKanji.setToolTip("Toggle Kanji")
        reader.menuView.insertAction(reader.menuView.actions()[2],self.actionToggleKanji)
        QtCore.QObject.connect(self.actionToggleKanji, QtCore.SIGNAL("toggled(bool)"), self.dockKanji.setVisible)


    def onVisibilityChanged(self,visible):
        self.actionToggleKanji.setChecked(self.dockKanji.isVisible())

        
    def onAnchorClicked(self, url):
        command, index = url.split(':')
        if command == "jisho":
            url = QtCore.QUrl(self.reader.preferences["linkToKanji"].format(index))
            QtGui.QDesktopServices().openUrl(url)
        else:
            index = int(index)
            commands = command.split("_")
            profile = commands.pop(0)
            self.runCommand(commands,index)
        
    def onLookup(self,d,lengthMatched):
        if self.dockKanji.isVisible():
            if 'japanese' in self.reader.languages:
                if lengthMatched == 0:
                    self.definitions = self.reader.languages['japanese'].findCharacters(d.contentSample[0])
                    if len(self.definitions) > 0:
                        lengthMatched = 1
                else:
                    self.definitions = self.reader.languages['japanese'].findCharacters(d.contentSample[:lengthMatched])
                self.updateDefinitions()
            self.reader.updateVocabDefs('kanji')
        return lengthMatched
        
    def onShowDialogPreferences(self,dialog):
        GenericProfile.onShowDialogPreferences(self,dialog)

        
    def runCommand(self,cmd,definition):
        if cmd[0] == "copy":
            QtGui.QApplication.clipboard().setText(u'{character}\t{kunyomi}\t{onyomi}\t{glossary}'.format(**definition))
        elif cmd[0] =="add":
            self.addFact(definition)
        
    
    def markup(self, definition):
        return {
        'character': definition['character'],
        'onyomi': definition['onyomi'],
        'kunyomi': definition['kunyomi'],
        'glossary': definition['glossary'],
        'summary': definition['character']
    }

    def buildDefBody(self, definition, index, query, allowOverwrite):
        links = '<a href="kanji_copy:{0}"><img src="qrc:///img/img/icon_copy_definition.png" align="right"></a>'.format(index)
        if (query is not None and query('kanji', definition, index)):
            links += '<a href="kanji_add:{0}"><img src="qrc:///img/img/icon_add_expression.png" align="right"></a>'.format(index)

        readings = ', '.join([definition['kunyomi'], definition['onyomi']])
        html = u"""
            <span class="links">{0}</span>
            <span class="expression"><a href="jisho:{1}">{1}</a><br></span>
            <span class="reading">[{2}]<br></span>
            <span class="glossary">{3}<br></span>
            <br clear="all">""".format(links, definition['character'], readings, definition['glossary'])

        return html
