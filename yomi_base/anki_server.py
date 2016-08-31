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