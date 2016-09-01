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
import os

class KanjiProfile(GenericProfile):
    name = "kanji"
    descriptor = "KANJI IN THIS TEXT"
    displayedName = "Kanji"
    languages = ["japanese"]
    sortIndex = 2
    allowedTags = ['character', 'onyomi', 'kunyomi', 'glossary','ongroup','words']

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
            self.reader.profiles["vocabulary"].onQuery([index])
            #url = QtCore.QUrl(self.reader.preferences["linkToKanji"].format(index))
            #QtGui.QDesktopServices().openUrl(url)
        else:
            index = int(index)
            commands = command.split("_")
            profile = commands.pop(0)
            self.runCommand(commands,self.definitions[index])
        
    def onLookup(self,d,lengthMatched):
        if self.dockKanji.isVisible():
            if 'japanese' in self.reader.languages:
                if lengthMatched == 0:
                    self.definitions = self.reader.languages['japanese'].findCharacters(d['contentSample'][0])
                    if len(self.definitions) > 0:
                        lengthMatched = 1
                else:
                    self.definitions = self.reader.languages['japanese'].findCharacters(d['contentSample'][:lengthMatched])
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
        elif cmd[0] == "addgroup":
            kanjigroups = os.path.join(self.reader.anki.collection().media.dir(),"Yomichan","KanjiGroups")
            if os.path.exists(kanjigroups):
                filename = os.path.join(kanjigroups,definition['ongroup']+".txt")
                with open(filename,'w') as fp:
                    content = u"""### REGEXP ###
.*[{0}]###v###
### SHUFFLE THIS TEXT ###""".format(definition['ongroup'])
                    fp.write(content.encode('utf-8'))
                    fp.close()
            d = dict()
            d['contentSample'] = definition['ongroup']
            self.onLookup(d,len(d['contentSample']))
            self.reader.profiles["vocabulary"].onQuery(list(definition['ongroup']))
        
    
    def markup(self, definition):
        allCards = self.reader.plugin.fetchAllCards()
        words = u",".join([x for x in allCards["vocabulary"].keys() if definition['character'] in x])
        return {
        'character': definition['character'],
        'onyomi': definition['onyomi'],
        'kunyomi': definition['kunyomi'],
        'glossary': definition['glossary'],
        'summary': definition['character'],
        'ongroup': definition['ongroup'],
        'words': words
    }

    def buildDefBody(self, definition, index, allowOverwrite):
        links = '<a href="kanji_copy:{0}"><img src="qrc:///img/img/icon_copy_definition.png" align="right"></a>'.format(index)
        if (self.ankiIsFactValid('kanji', definition, index)):
            links += '<a href="kanji_add:{0}"><img src="qrc:///img/img/icon_add_expression.png" align="right"></a>'.format(index)

        readings = ', '.join([definition['kunyomi'], definition['onyomi']])
        if definition['ongroup'] is not None:
            ongroup = u"""<a style="text-decoration:none;" href="kanji_addgroup:{0}">{1}</a>""".format(index,definition['ongroup'])
        else:
            ongroup = ''
        html = u"""
            <span class="links">{0}</span>
            <span class="expression"><a href="jisho:{1}">{1}</a><br></span>
            <span class="reading">[{2}]<br></span>
            <span class="glossary">{3}<br></span>
            <span class="ongroup">{4}<br></span>
            <br clear="all">""".format(links, definition['character'], readings, definition['glossary'],ongroup)

        return html
