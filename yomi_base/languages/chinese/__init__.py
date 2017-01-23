# -*- coding: utf-8 -*-

import dictionary
import os.path
import translate


def initLanguage(preferences,load=True):
    directory = os.path.dirname(__file__)
    dic = dictionary.Dictionary(os.path.join(directory, 'cedict_ts.u8'), load=load)
    if load:
        return translate.Translator(dic)
        
