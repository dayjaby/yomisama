# -*- coding: utf-8 -*-

import re


def isHangul(c):
    return 0xac00 <= ord(c) <= 0xd7a3

def isJamo(c):
    return 0x1100 <= ord(c) <= 0x11ff or 0x3130 <= ord(c) <= 0x318f or 0xa960 <= ord(c) <= 0xa97f or 0xd7b0 <= ord(c) <= 0xd7ff

def isHanja(c):
    return 0x4e00 <= ord(c) < 0x9fb0 or 0x3400 <= ord(c) < 0x4dc0


def isKorean(c):
    return isHangul(c) or isHanja(c)


def sanitize(text, noHanja=True, wildcards=False):
    if noHanja:
        checker = isKorean
    else:
        checker = isHanja        

    if wildcards:
        text = re.sub(u'[\*＊]', u'%', text)
        text = re.sub(u'[\?？]', u'_', text)
        overrides = [u'%', u'_']
    else:
        overrides = list()

    result = unicode()
    for c in text:
        if checker(c) or c in overrides:
            result += c
    for c in u' .,،、…‒–':
        result = (result+c)[:result.find(c)]
    return result
