# -*- coding: utf-8 -*-

import deinflect
import dictionary
import os.path
import translate


def initLanguage(preferences,load=True):
    directory = os.path.dirname(__file__)
    dic = dictionary.Dictionary(os.path.join(directory, 'dictionary.db'), load=load)
    if load:
        return translate.Translator(
            deinflect.Deinflector(os.path.join(directory, 'hangeul.js')),
            dic
        )
        
