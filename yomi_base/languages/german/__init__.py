# -*- coding: utf-8 -*-

from . import dictionary
import os.path
from . import translate


def initLanguage(preferences,load=True):
    directory = os.path.dirname(__file__)
    dic = dictionary.Dictionary(os.path.join(directory, 'de-eng.txt'), load=load)
    if load:
        return translate.Translator(None,dic)
        
