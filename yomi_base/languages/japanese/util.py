# -*- coding: utf-8 -*-

import re


def isHiragana(c):
    return 0x3040 <= ord(c) < 0x30a0


def isKatakana(c):
    return 0x30a0 <= ord(c) < 0x3100


def isKana(c):
    return isHiragana(c) or isKatakana(c)


def isKanji(c):
    return 0x4e00 <= ord(c) < 0x9fb0 or 0x3400 <= ord(c) < 0x4dc0


def isJapanese(c):
    return isKana(c) or isKanji(c)


def sanitize(ntext, kana=True, wildcards=False):
    if kana:
        checker = isJapanese
    else:
        checker = isKanji
    
    text = u''    
    lastchar = u'々'
    for i in ntext:
        if i != u'々':
            lastchar = i
        text += lastchar
        

    if wildcards:
        text = re.sub(u'[\*＊]', u'%', text)
        text = re.sub(u'[\?？]', u'_', text)
        overrides = [u'%', u'_']
    else:
        overrides = list()

    result = ""
    for c in text:
        if checker(c) or c in overrides:
            result += c

    return result
