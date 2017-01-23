# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import constants
import gen.updates_ui
import json
import urllib2


class DialogUpdates(QtGui.QDialog, gen.updates_ui.Ui_DialogUpdates):
    def __init__(self, parent, versions):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.updateHtml(versions)
        self.labelUpdates.setText(
            unicode(self.labelUpdates.text()).format(
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
            fp = urllib2.urlopen('http://cult-soft.de/yomisama/updates.json')
            updates = json.loads(fp.read())
            fp.close()

            for update in updates:
                latest = max(latest, update.get('version'))
        except:
            pass
        finally:
            self.updateResult.emit({ 'latest': latest, 'updates': updates })
