# -*- coding: utf-8 -*-

# Copyright (C) 2016  David Jablonski
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

from PyQt4 import QtCore
from ajax import AjaxServer
from constants import c


class AnkiConnect:
    def __init__(self, yomisama, preferences, interval=25):
        self.yomisama        = yomisama
        self.preferences = preferences
        self.server      = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.advance)
        self.timer.start(interval)


    def advance(self):
        enabled = self.preferences['enableAnkiConnect']

        if self.server is None and enabled:
            self.server = AjaxServer(self.handler)
            self.server.listen()
        elif self.server is not None and not enabled:
            self.server.close()
            self.server = None

        if self.server is not None:
            self.server.advance()


    def handler(self, request):
        action = 'api_' + (request.get('action') or '')
        if hasattr(self, action):
            return getattr(self, action)(request.get('params') or {})


    def api_lookup(self,params):
        htmls = dict()
        for profile in self.yomisama.window.getSortedProfiles():
            profile.onLookup(params,0)
            htmls[profile.name] = {'body':profile.defBody,'name':profile.displayedName};
        return htmls

    def api_link(self,params):
        self.yomisama.window.profiles[params["profile"]].onAnchorClicked(params["href"])
        htmls = dict()
        for profile in self.yomisama.window.getSortedProfiles():
            htmls[profile.displayedName] = profile.defBody
        return htmls
