# -*- coding: utf-8 -*-

# Copyright (C) 2016 David Jablonski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import BeautifulSoup
import urllib2
from PyQt4 import QtGui, QtCore
from aqt.webview import AnkiWebView
from profile import *
from .. import reader_util
from .. import preferences

class VocabKeyFilter(QtCore.QObject):
    obj = None
    
    def eventFilter(self, unused, event):
        obj = self.obj
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.buttons() & QtCore.Qt.MidButton or event.modifiers() & QtCore.Qt.ShiftModifier:
                obj.updateSampleFromSelection()
                return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == preferences.lookupKeys[obj.reader.preferences['lookupKey']][1]:
                obj.updateSampleFromSelection()
                return True
        return False

class VocabularyProfile(GenericProfile):
    name = "vocabulary"
    displayedName = "Vocabulary"
    descriptor = "VOCABULARY IN THIS TEXT (EXPORT)"
    languages = ["japanese","chinese","korean"]
    sortIndex = 1
    allowedTags = ['expression', 'kanji', 'hanja', 'reading', 'glossary', 'sentence','line','filename','summary','traditional','language','goo','defs','refs']

    def __init__(self,reader):
        GenericProfile.__init__(self,reader)
        self.history = []
        self.currentIndex = 0
        self.dockVocab = QtGui.QDockWidget(reader)
        self.dockVocab.setObjectName(fromUtf8("dockVocab"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(fromUtf8("verticalLayout"))
        self.previousExpression = None
        self.textField = AnkiWebView()
        self.textField.setAcceptDrops(False)
        self.textField.setObjectName("textField")
        self.keyFilter = VocabKeyFilter()
        self.keyFilter.obj = self
        self.keyFilter.textField = self.textField
        self.textField.installEventFilter(self.keyFilter)
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

        self.dockVocab.installEventFilter(self.reader.keyFilter)
        
    def updateSampleFromSelection(self):
        d = {
            "samplePosStart": 0,
            "contentSampleFlat": self.textField.selectedText(),
            "content": ""
        }
        self.onLookup(d,0,sentenceAndLine=False)
        
    def fixHtml(self,html,appendToHistory=True):
        if html.find(self.buildEmpty()) == -1 and appendToHistory:
            self.history.append(html)
        back = len(self.history)>1
        #self.currentIndex > 0
        #forward = self.currentIndex < len(self.history)-1
        if back:
            backHtml = "<a href='vocabulary_back:0'>&lt;&lt;Back</a>" if back else ""
            forwardHtml = ""
            #"<a href='vocabulary_forward:0'>Forward&gt;&gt;</a>" if forward else ""
            return u"<div>{1} {2}</div><br>{0}".format(html,backHtml,forwardHtml)
        else:
            return html
        
    def onVisibilityChanged(self,visible):
        self.actionToggleVocab.setChecked(self.dockVocab.isVisible())

        
    def onAnchorClicked(self, url):
        command, index = url.split(':')
        if command == "jisho":
            url = QtCore.QUrl(self.reader.preferences["linkToVocab"].format(index))
            QtGui.QDesktopServices().openUrl(url)
        elif command == "vocabulary_back":
            self.history.pop()
            html = self.fixHtml(self.history[-1],appendToHistory=False)
            self.textField.setHtml(html)
        elif command == "vocabulary_forward":
            self.textField.history().forward()
        else:
            if not index.startswith("void"):
                index = int(index)
                commands = command.split("_")
                profile = commands.pop(0)
                self.runCommand(commands,index)
        
    def onLookup(self,d,lengthMatched,sentenceAndLine=True):
        if self.dockVocab.isVisible():
            lengthMatched = self.reader.findTerm(d)
            if sentenceAndLine:
                sentence, sentenceStart = reader_util.findSentence(d['content'], d['samplePosStart'])
                line, lineStart  = reader_util.findLine(d['content'], d['samplePosStart'])
            else:
                sentence = line = ""
            for definition in self.definitions:
                definition['sentence'] = sentence
                definition['line'] = line
                definition['filename'] = self.reader.state.filename
            self.previousExpression = None
            self.reader.updateVocabDefs('vocabulary')
        return lengthMatched
        
    def onQuery(self,query):
        if self.dockVocab.isVisible():
            lengthMatched = self.reader.findTerm(query,wildcards=True)
            for definition in self.definitions:
                definition['sentence'] = ""
                definition['line'] = ""
                definition['filename'] = self.reader.state.filename
            self.previousExpression = None
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
                definition = definition.copy()
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
            'defs': definition.get("defs") or unicode(),
            'refs': definition.get("refs") or unicode(),
            'expression': definition['expression'],
            'hanja': definition.get('hanja') or unicode(),
            'reading': definition.get('reading') or unicode(),
            'glossary': definition.get('glossary') or unicode(),
            'gender': definition.get('gender') or unicode(),
            'language': definition.get('language') or unicode(),
            'sentence': definition.get('sentence') or unicode(),
            'traditional': definition.get('traditional') or unicode(),
            'line': definition.get('line') or unicode(),
            'filename': definition.get('filename') or unicode(),
            'goo': definition.get('goo') or unicode(),
            'summary': summary
        }

    def buildDefBody(self, definition, index, allowOverwrite):
        reading = unicode()
        if(definition.get('language') == 'Japanese' and (definition['expression']+"["+(definition['reading'] or "")+"]") in self.reader.preferences['onlineDicts']['goo']):
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
            
        gender = unicode()
        if definition.get('gender'):
            gender = '<span class="gender">{0}<br></span>'.format(definition['gender'])

        links = '<a href="vocabulary_copy:{0}"><img src="qrc:///img/img/icon_copy_definition.png" align="right"></a>'.format(index)
        markupExp = self.markup(definition)
        defReading = definition.copy()
        if defReading.get('reading'):
            defReading['expression'] = defReading['reading']
            del defReading['reading']
        markupReading = self.markup(defReading)
        if self.ankiIsFactValid('vocabulary', markupExp, index):
            links += u'<a href="vocabulary_add:{0}"><img src="qrc:///img/img/icon_add_expression.png" align="right"></a>'.format(index)
        else:
            if allowOverwrite:
                links += u'<a href="vocabulary_overwrite:{0}"><img src="qrc:///img/img/icon_overwrite_expression.png" align="right"></a>'.format(index)
        if markupReading is not None and definition.get('language') == 'Japanese':
            if self.ankiIsFactValid('vocabulary', markupReading, index):
                links += u'<a href="vocabulary_add_reading:{0}"><img src="qrc:///img/img/icon_add_reading.png" align="right"></a>'.format(index)
            elif markupExp is not None and markupReading['summary'] != markupExp['summary']:
                if allowOverwrite:
                    links += u'<a href="vocabulary_overwrite_reading:{0}"><img src="qrc:///img/img/icon_overwrite_reading.png" align="right"></a>'.format(index)

        def glossary(hide):
            if hide:
                return u"""<a onclick='document.getElementById("glossary{1}").style.display="block";this.style.display="none"' href="javascript:void(0);">[Show English]<br></a><span class="glossary" id="glossary{1}" style="display:none;">{0}<br></span>""".format(definition['glossary'],index)
            else:
                return u'<span class="glossary" id="glossary">{0}<br></span>'.format(definition['glossary'])
        foundOnlineDictEntry = False
        if markupExp["defs"] != "":
            dictionaryEntries = u"<span class='online'>"+ markupExp["defs"] + " " + markupExp["refs"] + "</span>"
            foundOnlineDictEntry = True
        else:
            dictionaryEntries = ""
        if(definition.get("goo")):
            dictionaryEntries += u"<br><span class='online'>" + definition["goo"] + "</span><br>"
            foundOnlineDictEntry = True
        elif(definition.get('language') == 'Japanese'):
            dictionaryEntries += u'<br><a href="vocabulary_goo:{0}">[Goo]</a><br>'.format(index)
        if(definition.get('language') == 'Japanese'):
            expression = u'<span class="expression"><a href="jisho:{0}">{0}</a></span>'.format(definition["expression"])
            reading = reading + '<br>'
        elif(definition.get('language') == 'German'):
            if self.previousExpression == definition['expression']:
                expression = ''
            else:
                expression = u'<span class="german">{0}</span><br>'.format(definition['expression'] + ' ' + gender)
                self.previousExpression = definition['expression']
        else:
            expression = u'<span class="expression">{0}</span>'.format(definition['expression'])
            reading = reading + '<br>'
        html = u"""
            <span class="links">{0}</span>
            {1}
            {2}
            {3}
            {4}
            {5}
            <br clear="all">""".format(links, expression, reading, glossary(foundOnlineDictEntry and self.reader.preferences['hideTranslation']), rules,dictionaryEntries)
        if (definition.get('language') != 'German'):
            html = u"<hr>" + html

        return html
