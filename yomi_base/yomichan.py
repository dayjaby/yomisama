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


from yomi_base.preference_data import Preferences
import urllib2

import aqt
from aqt.downloader import download
from aqt.utils import showInfo
from anki.hooks import addHook

class Yomichan:
    def __init__(self):
        self.languages = dict()
        self.preferences = Preferences()
        self.preferences.load()
        if not self.loadLanguages():
            def downloadDictionaries():
                showInfo(_("No Yomichan dictionaries found\nDownloading now"))
                ret = download(aqt.mw, 2027900559)
                if not ret:
                    raise Exception("Could not download dictionary files")
                data, fname = ret
                aqt.mw.addonManager.install(data, fname)
                aqt.mw.progress.finish()
            addHook('profileLoaded',downloadDictionaries)
        self.loadSubscriptions()

    def loadLanguages(self):
        languageFound = False
        languages = ["japanese","korean","chinese","german","spanish"]
        for language in languages:
            languageFound |= self.loadLanguage(language)

        return languageFound

    def loadLanguage(self,language,callback=None):
        try:
            module = getattr(__import__('yomi_base.languages.'+language, globals(), locals(), [], -1).languages,language)
            l = module.initLanguage(self.preferences, self.preferences.settings[language])
            if l:
                self.languages[language] = l
            return True
        except Exception as e:
            if callback:
                callback(e)
        return False
            
    def loadSubscriptions(self):
        for sub in self.preferences['subscriptions']:
            try:
                fp = urllib2.urlopen(sub['source'])
                f = open(sub['target'], 'w')
                f.write(fp.read())
                f.close()
                fp.close()
            except:
                donothing = True
        
    def fetchAllCards(self):
        return None
        
