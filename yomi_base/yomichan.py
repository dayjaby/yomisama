# -*- coding: utf-8 -*-

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
        
