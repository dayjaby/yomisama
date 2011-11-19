#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright (C) 2011  Alex Yatskov
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


import sys
from PyQt4 import QtGui, QtCore
from yomichan.lang import japanese
from yomichan.util import buildResPath
from yomichan.preference_data import Preferences
from yomichan.reader import MainWindowReader


class Yomichan:
    def __init__(self):
        self.languages = {'Japanese': japanese.initLanguage()}
        self.preferences = Preferences()
        self.preferences.load()


class YomichanPlugin(Yomichan):
    def __init__(self):
        Yomichan.__init__(self)

        self.toolIconVisible = False
        self.window = None
        self.anki = anki_host.Anki()
        self.parent = self.anki.window()
        self.separator = QtGui.QAction(self.parent)
        self.separator.setSeparator(True)
        self.action = QtGui.QAction(QtGui.QIcon(buildResPath('img/logo32x32.png')), '&Yomichan...', self.parent)
        self.action.setIconVisibleInMenu(True)
        self.parent.connect(self.action, QtCore.SIGNAL('triggered()'), self.onShowRequest)

        self.anki.addHook('loadDeck', self.onDeckLoad)
        self.anki.addHook('deckClosed', self.onDeckClose)


    def onShowRequest(self):
        if self.window:
            self.window.setVisible(True)
            self.window.activateWindow()
        else:
            self.window = MainWindowReader(
                self.parent,
                self.preferences,
                self.languages,
                None,
                self.anki,
                self.onWindowClose,
                self.onWindowUpdate
            )
            self.window.show()


    def onWindowClose(self):
        self.window = None


    def onWindowUpdate(self):
        if self.preferences.ankiShowIcon:
            self.showToolIcon()
        else:
            self.hideToolIcon()


    def onDeckLoad(self):
        self.anki.toolsMenu().addAction(self.separator)
        self.anki.toolsMenu().addAction(self.action)

        if self.preferences.ankiShowIcon:
            self.showToolIcon()


    def onDeckClose(self):
        self.anki.toolsMenu().removeAction(self.action)
        self.anki.toolsMenu().removeAction(self.separator)

        self.hideToolIcon()

        if self.window:
            self.window.close()
            self.window = None


    def hideToolIcon(self):
        if self.toolIconVisible:
            self.anki.toolBar().removeAction(self.action)
            self.toolIconVisible = False


    def showToolIcon(self):
        if not self.toolIconVisible:
            self.anki.toolBar().addAction(self.action)
            self.toolIconVisible = True


class YomichanStandalone(Yomichan):
    def __init__(self):
        Yomichan.__init__(self)

        self.application = QtGui.QApplication(sys.argv)
        self.window = MainWindowReader(
            None,
            self.preferences,
            self.languages,
            filename=sys.argv[1] if len(sys.argv) >= 2 else None
        )
        self.window.show()
        self.application.exec_()


if __name__ == '__main__':
    instance = YomichanStandalone()
else:
    from yomichan import anki_host
    instance = YomichanPlugin()