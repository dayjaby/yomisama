# -*- coding: utf-8 -*-

from PyQt6 import QtCore, QtWidgets
from . import constants
from .gen import updates
import json
from urllib.request import urlopen


class DialogUpdates(QtWidgets.QDialog, updates.Ui_DialogUpdates):
    def __init__(self, parent, versions):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.updateHtml(versions)
        self.labelUpdates.setText(
            self.labelUpdates.text().format(
                constants.c['appVersion'],
                versions['latest']
            )
        )


    def updateHtml(self, versions):
        html = '<html><body>'

        for update in versions['updates']:
            version = update.get('version')
            if version > constants.c['appVersion']:
                html += '<strong>Version {0}</strong>'.format(version)
                html += '<ul>'
                for feature in update['features']:
                    html += '<li>{0}</li>'.format(feature)
                html += '</ul>'

        self.textBrowser.setHtml(html)


class UpdateFinder(QtCore.QThread):
    updateResult = QtCore.pyqtSignal(dict)

    def run(self):
        latest = constants.c['appVersion']
        updates = list()

        try:
            fp = urlopen('http://cult-soft.de/yomisama/updates.json')
            updates = json.loads(fp.read())
            fp.close()

            for update in updates:
                latest = max(latest, update.get('version'))
        except:
            pass
        finally:
            self.updateResult.emit({ 'latest': latest, 'updates': updates })
