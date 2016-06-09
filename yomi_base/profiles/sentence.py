from aqt.webview import AnkiWebView
from PyQt4 import QtGui
from profile import *
from .. import reader_util

class SentenceProfile(GenericProfile):
    name = "sentence"
    displayedName = "Sentence"
    descriptor = "SENTENCES IN THIS TEXT"
    languages = ["japanese","chinese","korean"]
    sortIndex = 3
    allowedTags = ['text','filename']

    def __init__(self,reader):
        GenericProfile.__init__(self,reader)
        
        self.dockSentence = QtGui.QDockWidget(reader)
        self.dockSentence.setObjectName(fromUtf8("dockSentence"))
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
        self.dockSentence.setWidget(self.dockWidgetContents)
        reader.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockSentence)
        self.dockSentence.visibilityChanged.connect(self.onVisibilityChanged)
        self.dockSentence.setWindowTitle(translate("MainWindowReader", "Sentence", None))
        self.textField.setLinkHandler(self.onAnchorClicked)


        # menu entries to toggle visibility of the Sentence dock
        self.actionToggleSentence = QtGui.QAction(reader)
        self.actionToggleSentence.setCheckable(True)
        self.actionToggleSentence.setObjectName("actionToggleSentence")
        self.actionToggleSentence.setText("&Sentence")
        self.actionToggleSentence.setToolTip("Toggle Sentence")
        reader.menuView.insertAction(reader.menuView.actions()[2],self.actionToggleSentence)
        QtCore.QObject.connect(self.actionToggleSentence, QtCore.SIGNAL("toggled(bool)"), self.dockSentence.setVisible)
        
    def onAnchorClicked(self, url):
        command, index = url.split(':')
        index = int(index)
        commands = command.split("_")
        profile = commands.pop(0)
        self.runCommand(commands,index)

    def onVisibilityChanged(self,visible):
        self.actionToggleSentence.setChecked(self.dockSentence.isVisible())

        
    def onLookup(self,d,lengthMatched):
        if self.dockSentence.isVisible():
            lengthMatched = self.reader.findTerm(d.contentSampleFlat)
            sentence, sentenceStart = reader_util.findSentence(d.content, d.samplePosStart)
            line, lineStart = reader_util.findLine(d.content, d.samplePosStart)
            self.definitions = [{
                'text': sentence,
                'filename': self.reader.state.filename
            },{
                'text': line,
                'filename': self.reader.state.filename
            }]
            self.updateDefinitions()
            self.reader.updateVocabDefs('sentence')
        return lengthMatched

        
    def onShowDialogPreferences(self,dialog):
        GenericProfile.onShowDialogPreferences(self,dialog)
        
    def runCommand(self,cmds,index):
        if index >= len(self.definitions):
            return
        definition = self.definitions[index]
        if cmds[0] == "add":
            self.addFact(definition)
        elif cmds[0] == "overwrite":
            self.overwriteFact(definition)
            
    def markup(self,definition):
        d = dict(definition)
        d['summary'] = d['text']
        return d


    def buildDefBody(self, definition, index, existsAlready, allowOverwrite):
        links = ""
        if existsAlready is not None:
            if existsAlready('sentence', self.markup(definition), index):
                links += '<a href="sentence_add:{0}"><img src="qrc:///img/img/icon_add_expression.png" align="right"></a>'.format(index)
            else:
                if allowOverwrite:
                    links += '<a href="sentence_overwrite:{0}"><img src="qrc:///img/img/icon_overwrite_expression.png" align="right"></a>'.format(index)
        html = ("<b>Sentence: </b><br>" if index == 0 else "<b>Line: </b><br>") + u"""
            <span class="sentence">{0}{1}<br></span>
            <br clear="all">""".format(definition.get('text') or unicode(), links)

        return html