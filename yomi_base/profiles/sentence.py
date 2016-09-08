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

from aqt.webview import AnkiWebView
from PyQt4 import QtGui
from profile import *
from .. import reader_util
import BeautifulSoup

import urllib
import urllib2

class SentenceProfile(GenericProfile):
    name = "sentence"
    displayedName = "Sentence"
    descriptor = "SENTENCES IN THIS TEXT"
    languages = ["japanese","chinese","korean"]
    sortIndex = 3
    allowedTags = ['text','filename','translation']

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
        if url == "kotonoha":
            prefix = "http://www.kotonoha.gr.jp"
            link = prefix + "/shonagon/search_result"
            data = [
                ("lcontext_regex",""),
                ("rcontext_regex",""),
                ("entire_period","1"),
                ("media",u"書籍".encode("utf-8")),
                ("media",u"雑誌".encode("utf-8")),
                ("media",u"新聞".encode("utf-8")),
                ("media",u"白書".encode("utf-8")),
                ("media",u"教科書".encode("utf-8")),
                ("media",u"広報紙".encode("utf-8")),
                ("media",u"Yahoo!知恵袋".encode("utf-8")),
                ("media",u"Yahoo!ブログ".encode("utf-8")),
                ("media",u"韻文".encode("utf-8")),
                ("media",u"法律".encode("utf-8")),
                ("media",u"国会会議録".encode("utf-8")),
                ("query_string",self.reader.getSample().encode("utf-8"))
            ]
            data = urllib.urlencode(data)
            self.data = data
            
            page = urllib2.urlopen(
              urllib2.Request(url=link,data=data,
              headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})).read()
            soup = BeautifulSoup.BeautifulSoup(page)
            self.soup = unicode(soup)
            trs = soup.find("table",id="tablekit-table-1").findAll("tr")[1:]
            self.definitionType = "kotonoha"
            self.definitions = []
            for tr in trs:
                tds = tr.findAll("td")[1:3]
                row = ''.join(map(unicode,tds))
                self.definitions.append({
                    'text': row,
                    'filename': self.reader.state.filename,
                    'translation': ''
                })
            self.updateDefinitions()
            self.reader.updateVocabDefs('sentence')
        else:
            command, index = url.split(':')
            index = int(index)
            commands = command.split("_")
            profile = commands.pop(0)
            self.runCommand(commands,index)

    def onVisibilityChanged(self,visible):
        self.actionToggleSentence.setChecked(self.dockSentence.isVisible())

        
    def onLookup(self,d,lengthMatched):
        if self.dockSentence.isVisible():
            sentence, sentenceStart = reader_util.findSentence(d['content'], d['samplePosStart'])
            line, lineStart = reader_util.findLine(d['content'], d['samplePosStart'])
            self.definitionType = "normal"
            self.definitions = [{
                'text': sentence,
                'filename': self.reader.state.filename,
                'translation': ''
            },{
                'text': line,
                'filename': self.reader.state.filename,
                'translation': ''
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


    def buildDefBody(self, definition, index, allowOverwrite):
        links = ""
        if self.ankiIsFactValid('sentence', self.markup(definition), index):
            self.existsAlready[index] = False
            links += '<a href="sentence_add:{0}"><img src="qrc:///img/img/icon_add_expression.png" align="right"></a>'.format(index)
        else:
            self.existsAlready[index] = True
            #links += '<a href="sentence_add:{0}"><img src="qrc:///img/img/icon_add_expression.png" align="right"></a>'.format(index)
            if allowOverwrite:
                links += '<a href="sentence_overwrite:{0}"><img src="qrc:///img/img/icon_overwrite_expression.png" align="right"></a>'.format(index)

        if hasattr(self,'definitionType') and self.definitionType == "normal":
            html = ("<b>Sentence: </b><br>" if index == 0 else "<b>Line: </b><br>") 
        else:
            html = ""
        html = html + u"""
            <span class="sentence">{0}{1}<br>{2}</span>
            <br clear="all">""".format(definition.get('text') or unicode(),
                                       links,definition.get('translation'))
        
        #html = u"""<a href='kotonoha'>[Kotonoha]</a><br>""" + html

        return html
