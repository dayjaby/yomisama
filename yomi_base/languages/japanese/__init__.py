# -*- coding: utf-8 -*-

import deinflect
import dictionary
import os.path
import translate

def initLanguage(preferences,load=True):
    directory = os.path.dirname(__file__)
    if os.path.isabs(preferences["japaneseDict"]):
        filename = preferences["japaneseDict"]
    else:
        filename = os.path.join(directory,preferences["japaneseDict"])
    dic = dictionary.Dictionary(filename, load=load)
    if load:
        return translate.Translator(
            deinflect.Deinflector(os.path.join(directory, 'deinflect.json')),
            dic
        )
        
