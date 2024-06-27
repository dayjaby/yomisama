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

import bs4 as BeautifulSoup
# from urllib.request import urlopen
import requests
from PyQt5 import QtWidgets, QtCore
from aqt.webview import AnkiWebView
from .profile import *
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
    allowedTags = ['expression', 'term', 'source', 'kanji', 'hanja', 'reading', 'glossary', 'sentence','line','filename','summary','traditional','language','goo','defs','refs']

    def __init__(self,reader):
        GenericProfile.__init__(self,reader)
        self.user_agent_headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        self.history = []
        self.currentIndex = 0
        self.dockVocab = QtWidgets.QDockWidget(reader)
        self.dockVocab.setObjectName(fromUtf8("dockVocab"))
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName(fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
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
        self.textField.onBridgeCmd = self.onAnchorClicked

        # menu entries to toggle visibility of the vocabulary dock
        self.actionToggleVocab = QtWidgets.QAction(reader)
        self.actionToggleVocab.setCheckable(True)
        self.actionToggleVocab.setObjectName("actionToggleVocab")
        self.actionToggleVocab.setText("&Vocabulary")
        self.actionToggleVocab.setToolTip("Toggle vocabulary")
        reader.menuView.insertAction(reader.menuView.actions()[2],self.actionToggleVocab)
        self.actionToggleVocab.toggled.connect(self.dockVocab.setVisible)
        self.dockVocab.installEventFilter(self.reader.keyFilter)

    def updateSampleFromSelection(self):
        d = {
            "samplePosStart": 0,
            "contentSampleFlat": self.textField.selectedText(),
            "content": ""
        }
        self.onLookup(d,0,sentenceAndLine=False)

    def fixHtml(self, html, appendToHistory=True):
        if html.find(self.buildEmpty()) == -1 and appendToHistory:
            self.history.append((html,list(self.definitions),self.defBody))
        back = len(self.history)>1
        #self.currentIndex > 0
        #forward = self.currentIndex < len(self.history)-1
        if back:
            backHtml = "<a href='#' onclicked='vocabulary_back:0'>&lt;&lt;Back</a>" if back else ""
            forwardHtml = ""
            #"<a href='vocabulary_forward:0'>Forward&gt;&gt;</a>" if forward else ""
            return u"<div>{1} {2}</div><br>{0}".format(html, backHtml, forwardHtml)
        else:
            return html

    def onVisibilityChanged(self,visible):
        self.actionToggleVocab.setChecked(self.dockVocab.isVisible())

    def onAnchorClicked(self, url):
        print(url)
        command, index = url.split(':')
        if command == "jisho":
            pass
            # url = QtCore.QUrl(self.reader.preferences["linkToVocab"].format(index))
            # QtWidgets.QDesktopServices().openUrl(url)
        elif command == "vocabulary_back":
            if len(self.history)>1:
                self.history.pop()
                html, definitions, body = self.history[-1]
                html = self.fixHtml(html, appendToHistory=False)
                self.textField.setHtml(html)
                self.definitions = definitions
                self.defBody = body
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
        dialog.checkHideTranslation = QtWidgets.QCheckBox(dialog.tabAnki)
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
            if definition.get("defs"):
                text = self.reader.textContent.toPlainText() + "\n"
                self.reader.textContent.setPlainText(text +
                                                     definition.get("defs").replace(u"<br>",u"\n"))

            QtWidgets.QApplication.clipboard().setText(result)
        elif cmds[0] == "goo":
            prefix = "http://dictionary.goo.ne.jp"
            self.reader.link = prefix + "/srch/jn/" + definition['expression'] + "/m1u/"
            print(prefix + "/srch/jn/" + definition['expression'] + "/m1u/")
            page = requests.get(
              prefix + "/srch/jn/" + definition['expression'] + "/m1u/",
              headers=self.user_agent_headers
            )
            if page.status_code == 200:
                soup = BeautifulSoup.BeautifulSoup(page.content, features="html.parser")
                if not soup.find("div", "contents-wrap-b"):
                    lis = soup.find("div", id="NR-main").find("div", "example_sentence").find("ul", "content_list").findAll("li")
                    for li in lis:
                        hiragana = li.find("p","title").contents[0].replace("・", "").replace("‐", "")
                        idx = hiragana.find("【")
                        if idx>-1:
                            hiragana = hiragana[:idx]
                        self.reader.hiragana = [hiragana, definition['reading']]
                        self.reader.html = soup.contents[0]
                        if hiragana == definition['reading']:
                            a = li.find("a")
                            link = prefix + dict(a.attrs)["href"]
                            print(link)
                            page2 = requests.get(
                                url=link,
                                headers=self.user_agent_headers
                            )
                            if page2.status_code == 200:
                                soup = BeautifulSoup.BeautifulSoup(page2.content, features="html.parser")
                # "else" does not work here, because we might have changed the soup
                wrapb = soup.find("div", "contents-wrap-b")
                if wrapb:
                    goo_definition = ""
                    ols = wrapb.findAll("ol", "meaning")
                    if len(ols) > 0:
                        for meaning in ols:
                            goo_definition += str(meaning.find("li").find("p"))
                    else:
                        goo_definition = str(wrapb.find("div", "contents"))

                    definition['goo'] = goo_definition
                    self.reader.preferences['onlineDicts']['goo'][definition['expression']+"["+(definition['reading'] or "")+"]"] = definition['goo']
                    self.updateDefinitions()
        else:
            if len(cmds) > 1 and cmds[1] == "reading":
                definition = definition.copy()
                definition['summary'] = definition['reading']
                definition['expression'] = definition['reading']
                definition['reading'] = ""
            if cmds[0] == "add":
                self.addFact(definition)
            elif cmds[0] == "overwrite":
                self.overwriteFact(definition)
            elif cmds[0] == "overwrite_reading":
                # not implemented
                pass

    def markup(self, definition):
        if definition.get('reading'):
            summary = u'{expression}[{reading}]'.format(**definition)
        else:
            summary = u'{expression}'.format(**definition)

        return {
            'defs': definition.get("defs") or "",
            'refs': definition.get("refs") or "",
            'expression': definition['expression'],
            'hanja': definition.get('hanja') or "",
            'reading': definition.get('reading') or "",
            'glossary': definition.get('glossary') or "",
            'gender': definition.get('gender') or "",
            'language': definition.get('language') or "",
            'sentence': definition.get('sentence') or "",
            'traditional': definition.get('traditional') or "",
            'line': definition.get('line') or "",
            'filename': definition.get('filename') or "",
            'goo': definition.get('goo') or "",
            'term': definition.get('term') or "",
            'source': definition.get('source') or "",
            'summary': summary
        }

    def buildDefBody(self, definition, index, allowOverwrite):
        reading = ""
        if(definition.get('language') == 'Japanese' and (definition['expression']+"["+(definition['reading'] or "")+"]") in self.reader.preferences['onlineDicts']['goo']):
            definition['goo'] = self.reader.preferences['onlineDicts']['goo'][definition['expression']+"["+(definition['reading'] or "")+"]"]

        if definition.get('reading'):
            reading = u'<span class="reading">[{0}]<br>'.format(definition['reading'])
            if definition.get('tags') == u'traditional':
                reading += u' (trad.)'
            reading += '</span>'

        rules = ""
        if definition.get('rules'):
            rules = ' &lt; '.join(definition['rules'])
            rules = '<span class="rules">({0})<br></span>'.format(rules)

        gender = ""
        if definition.get('gender'):
            gender = '<span class="gender">{0}<br></span>'.format(definition['gender'])

        links = """<a href='#' onclick='pycmd(\"{0}:{1}\")'><img src="qrc:///img/img/icon_copy_definition.png" align="right"/></a>""".format("vocabulary_copy", index)
        markupExp = self.markup(definition)
        defReading = definition.copy()
        if defReading.get('reading'):
            defReading['expression'] = defReading['reading']
            del defReading['reading']
        markupReading = self.markup(defReading)
        if self.ankiIsFactValid('vocabulary', markupExp, index):
            links += """<a href='#' onclick='pycmd(\"{0}:{1}\")'><img src="qrc:///img/img/icon_add_expression.png" align="right"/></a>""".format("vocabulary_add", index)
        else:
            if allowOverwrite:
                links += """<a href='#' onclick='pycmd(\"{0}:{1}\")'><img src="qrc:///img/img/icon_overwrite_expression.png" align="right"/></a>""".format("vocabulary_overwrite", index)
        if markupReading is not None and definition.get('language') == 'Japanese':
            if self.ankiIsFactValid('vocabulary', markupReading, index):
                links += """<a href='#' onclick='pycmd(\"{0}:{1}\")'><img src="qrc:///img/img/icon_add_reading.png" align="right"/></a>""".format("vocabulary_add_reading", index)
            elif markupExp is not None and markupReading['summary'] != markupExp['summary']:
                if allowOverwrite:
                    links += """<a href='#' onclick='pycmd(\"{0}:{1}\")'><img src="qrc:///img/img/icon_overwrite_reading.png" align="right"/></a>""".format("vocabulary_overwrite_reading", index)

        def glossary(hide):
            if hide:
                return """<a href='#' onclick='document.getElementById("glossary{1}").style.display="block";this.style.display="none"' href="javascript:void(0);">[Show English]<br></a><span class="glossary" id="glossary{1}" style="display:none;">{0}<br></span>""".format(definition['glossary'], index)
            else:
                return '<span class="glossary" id="glossary">{0}<br></span>'.format(definition['glossary'])
        foundOnlineDictEntry = False
        if markupExp["defs"] != "":
            dictionaryEntries = "<span class='online'>"+ markupExp["defs"] + " " + markupExp["refs"] + "</span>"
            foundOnlineDictEntry = True
        else:
            dictionaryEntries = ""
        if(definition.get("goo")):
            dictionaryEntries += "<br><span class='online'>" + definition["goo"] + "</span><br>"
            foundOnlineDictEntry = True
        elif(definition.get('language') == 'Japanese'):
            dictionaryEntries += """<br><a href='#' onclick='pycmd("{0}:{1}")'>[Goo]</a><br>""".format("vocabulary_goo", index)
        if(definition.get('language') == 'Japanese'):
            expression = """<span class='expression'><a href='#' onclick='pycmd("jisho:{0}")'>{0}</a></span>""".format(definition["expression"])
            reading = reading + "<br>"
        elif(definition.get('language') == 'German'):
            if self.previousExpression == definition['expression']:
                expression = ""
            else:
                expression = "<span class='german'>{0}</span><br>".format(definition['expression'] + " " + gender)
                self.previousExpression = definition['expression']
        else:
            expression = "<span class='expression'>{0}</span>".format(definition['expression'])
            reading = reading + '<br>'
        html = u"""
            {1}
            {2}
            <span class="links">{0}</span>
            {3}
            {4}
            {5}
            <br clear="all">""".format(links, expression, reading, glossary(foundOnlineDictEntry and self.reader.preferences['hideTranslation']), rules,dictionaryEntries)
        if (definition.get('language') != 'German'):
            html = u"<hr>" + html

        return html
