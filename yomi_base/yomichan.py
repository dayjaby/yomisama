# -*- coding: utf-8 -*-

from .preference_data import Preferences
from urllib.request import urlopen

import importlib
import aqt
from aqt.downloader import download
from aqt.utils import showInfo
from anki.hooks import addHook

from .languages import japanese, korean, chinese #, german, spanish

languages = {
    "japanese": japanese,
    "korean": korean,
    "chinese": chinese
}

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
            # addHook('profileLoaded',downloadDictionaries)
        self.loadSubscriptions()

    def loadLanguages(self):
        languageFound = False
        for language in languages.keys():
            languageFound |= self.loadLanguage(language)

        return languageFound

    def loadLanguage(self, language, callback=None):
        module = languages[language]
        try:
            l = module.initLanguage(self.preferences, self.preferences.settings[language])
            if l:
                self.languages[language] = l
            return True
        except Exception as e:
            print(str(e))
            if callback:
                callback(e)
        return False
            
    def loadSubscriptions(self):
        for sub in self.preferences['subscriptions']:
            try:
                fp = urlopen(sub['source'])
                f = open(sub['target'], 'w')
                f.write(fp.read())
                f.close()
                fp.close()
            except:
                donothing = True
        
    def fetchAllCards(self):
        return None
        
