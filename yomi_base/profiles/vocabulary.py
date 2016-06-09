import BeautifulSoup
import urllib2
from PyQt4 import QtGui, QtCore
from aqt.webview import AnkiWebView
from profile import *
from .. import reader_util

class VocabularyProfile(GenericProfile):
    name = "vocabulary"
    displayedName = "Vocabulary"
    descriptor = "VOCABULARY IN THIS TEXT (EXPORT)"
    languages = ["japanese","chinese","korean"]
    sortIndex = 1
    allowedTags = ['expression', 'kanji', 'hanja', 'reading', 'glossary', 'sentence','line','filename','summary','traditional','language','goo']

    def __init__(self,reader):
        GenericProfile.__init__(self,reader)
        
        self.dockVocab = QtGui.QDockWidget(reader)
        self.dockVocab.setObjectName(fromUtf8("dockVocab"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(fromUtf8("verticalLayout"))
        self.textField = AnkiWebView()
        self.textField.setAcceptDrops(False)
        self.textField.setObjectName("textField")
        self.verticalLayout.addWidget(self.textField)
        self.dockVocab.setWidget(self.dockWidgetContents)
        reader.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockVocab)
        self.dockVocab.visibilityChanged.connect(self.onVisibilityChanged)
        self.dockVocab.setWindowTitle(translate("MainWindowReader", "Vocabulary", None))
        self.textField.setLinkHandler(self.onAnchorClicked)

        # menu entries to toggle visibility of the vocabulary dock
        self.actionToggleVocab = QtGui.QAction(reader)
        self.actionToggleVocab.setCheckable(True)
        self.actionToggleVocab.setObjectName("actionToggleVocab")
        self.actionToggleVocab.setText("&Vocabulary")
        self.actionToggleVocab.setToolTip("Toggle vocabulary")
        reader.menuView.insertAction(reader.menuView.actions()[2],self.actionToggleVocab)
        QtCore.QObject.connect(self.actionToggleVocab, QtCore.SIGNAL("toggled(bool)"), self.dockVocab.setVisible)

    def onVisibilityChanged(self,visible):
        self.actionToggleVocab.setChecked(self.dockVocab.isVisible())

        
    def onAnchorClicked(self, url):
        command, index = url.split(':')
        if command == "jisho":
            url = QtCore.QUrl(self.reader.preferences["linkToVocab"].format(index))
            QtGui.QDesktopServices().openUrl(url)
        else:
            index = int(index)
            commands = command.split("_")
            profile = commands.pop(0)
            self.runCommand(commands,index)
        
    def onLookup(self,d,lengthMatched):
        if self.dockVocab.isVisible():
            lengthMatched = self.reader.findTerm(d.contentSampleFlat)
            sentence, sentenceStart = reader_util.findSentence(d.content, d.samplePosStart)
            line, lineStart  = reader_util.findLine(d.content, d.samplePosStart)
            for definition in self.definitions:
                definition['sentence'] = sentence
                definition['line'] = line
                definition['filename'] = self.reader.state.filename
            self.reader.updateVocabDefs('vocabulary')
        return lengthMatched
        
    def onShowDialogPreferences(self,dialog):
        dialog.checkHideTranslation = QtGui.QCheckBox(dialog.tabAnki)
        dialog.checkHideTranslation.setObjectName(fromUtf8("checkHideTranslation"))
        dialog.verticalLayout_2.addWidget(dialog.checkHideTranslation)
        dialog.checkHideTranslation.setText(translate("DialogPreferences", "Hide translation, when an online dictionary entry is present", None))
        GenericProfile.onShowDialogPreferences(self,dialog)
        
        
    def runCommand(self,cmds,index):
        if index >= len(self.definitions):
            return
        definition = self.definitions[index]
        if cmds[0] == "copy":
            if definition['reading']:
                result = u'{expression}\t{reading}\t{glossary}\n'.format(**definition)
            else:
                result = u'{expression}\t{glossary}\n'.format(**definition)

            QtGui.QApplication.clipboard().setText(result)
        elif cmds[0] == "goo":
            prefix = "http://dictionary.goo.ne.jp"
            self.reader.link = prefix + "/srch/jn/" + definition['expression'] + "/m1u/"
            page = urllib2.urlopen(
              urllib2.Request(url=prefix + "/srch/jn/" + definition['expression'] + "/m1u/",
              headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})).read()
            soup = BeautifulSoup.BeautifulSoup(page)
            if not soup.find("div","contents-wrap-b"):
                lis = soup.find("div",id="NR-main").find("div","contents-wrap-a-in search").find("ul","list-search-a").findAll("li")
                for li in lis:
                    hiragana = li.find("dt","search-ttl-a").contents[0].replace(u"\u2010",u"").replace(u"\u30fb",u"")
                    idx = hiragana.find(u"\u3010")
                    if idx>-1:
                        hiragana = hiragana[:idx]
                    self.reader.hiragana = [hiragana,definition['reading']]
                    self.reader.html = soup.contents[0]
                    if hiragana == definition['reading']:
                        a = li.find("a")
                        link = prefix + dict(a.attrs)["href"]
                        page2 = urllib2.urlopen(
                          urllib2.Request(url=link,
                          headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})).read()
                        soup = BeautifulSoup.BeautifulSoup(page2)
            if soup.find("div","contents-wrap-b"):
                definition['goo'] = '\n'.join(map(unicode,soup.findAll("ol","list-data-b")))
                self.reader.preferences['onlineDicts']['goo'][definition['expression']+"["+(definition['reading'] or "")+"]"] = definition['goo']
                self.updateDefinitions()
        else:
            if len(cmds)>1 and cmds[1] == "reading":
                definition['summary'] = definition['reading']
                definition['expression'] = definition['reading']
                definition['reading'] = unicode()
                
            if cmds[0] == "add":
                self.addFact(definition)
            elif cmds[0] == "overwrite":
                self.overwriteFact(definition)
        
        
    
    def markup(self, definition):
        if definition.get('reading'):
            summary = u'{expression}[{reading}]'.format(**definition)
        else:
            summary = u'{expression}'.format(**definition)

        return {
            'expression': definition['expression'],
            'hanja': definition.get('hanja') or unicode(),
            'reading': definition.get('reading') or unicode(),
            'glossary': definition.get('glossary') or unicode(),
            'language': definition.get('language') or unicode(),
            'sentence': definition.get('sentence') or unicode(),
            'traditional': definition.get('traditional') or unicode(),
            'line': definition.get('line') or unicode(),
            'filename': definition.get('filename') or unicode(),
            'goo': definition.get('goo') or unicode(),
            'summary': summary
        }

    def buildDefBody(self, definition, index, existsAlready, allowOverwrite):
        reading = unicode()
        if((definition['expression']+"["+(definition['reading'] or "")+"]") in self.reader.preferences['onlineDicts']['goo']):
            definition['goo'] = self.reader.preferences['onlineDicts']['goo'][definition['expression']+"["+(definition['reading'] or "")+"]"]

        if definition.get('reading'):
            reading = u'<span class="reading">[{0}]<br>'.format(definition['reading'])
            if definition.get('tags') == u'traditional':
                reading += u' (trad.)'
            reading += '</span>'

        rules = unicode()
        if definition.get('rules'):
            rules = ' &lt; '.join(definition['rules'])
            rules = '<span class="rules">({0})<br></span>'.format(rules)

        links = '<a href="vocabulary_copy:{0}"><img src="qrc:///img/img/icon_copy_definition.png" align="right"></a>'.format(index)
        if existsAlready is not None:
            markupExp = self.markup(definition)
            defReading = definition.copy()
            if defReading.get('reading'):
                del defReading['reading']
            markupReading = self.markup(defReading)
            if existsAlready('vocabulary', markupExp, index):
                links += '<a href="vocabulary_add:{0}"><img src="qrc:///img/img/icon_add_expression.png" align="right"></a>'.format(index)
            else:
                if allowOverwrite:
                    links += '<a href="vocabulary_overwrite:{0}"><img src="qrc:///img/img/icon_overwrite_expression.png" align="right"></a>'.format(index)
            if markupReading is not None:
                if existsAlready('vocabulary', markupReading, index):
                    links += '<a href="vocabulary_add_reading:{0}"><img src="qrc:///img/img/icon_add_reading.png" align="right"></a>'.format(index)
                elif markupExp is not None and markupReading['summary'] != markupExp['summary']:
                    if allowOverwrite:
                        links += '<a href="vocabulary_overwrite_reading:{0}"><img src="qrc:///img/img/icon_overwrite_reading.png" align="right"></a>'.format(index)
        glossary = definition['glossary']
        foundOnlineDictEntry = False
        dictionaryEntries = ""
        if(definition.get("goo")):
            dictionaryEntries += "<span class='online'>" + definition["goo"] + "</span>"
            foundOnlineDictEntry = True
        else:
            dictionaryEntries = '<a href="vocabulary_goo:{0}">[Goo]</a>'.format(index)
        if foundOnlineDictEntry and self.reader.preferences['hideTranslation']:
            glossary = ""
        html = u"""
            <span class="links">{0}</span>
            <span class="expression"><a href="jisho:{1}">{1}</a><br></span>
            {2}
            <span class="glossary">{3}<br></span>
            {4}{5}
            <br clear="all">""".format(links, definition['expression'], reading, glossary, rules,dictionaryEntries)

        return html