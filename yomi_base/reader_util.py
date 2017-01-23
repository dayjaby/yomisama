# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import re
import codecs
import sqlite3


def decodeContent(content):
    encodings = ['utf-8', 'shift_jis', 'euc-jp', 'utf-16']
    errors = dict()

    for encoding in encodings:
        try:
            return content.decode(encoding), encoding
        except UnicodeDecodeError, e:
            errors[encoding] = e[2]

    encoding = sorted(errors, key=errors.get, reverse=True)[0]
    return content.decode(encoding, 'replace'), encoding


def stripReadings(content):
    return re.sub(u'《[^》]+》', unicode(), content)

def findLine(content, position):
    startLine = content[0:position].rfind(u'\n')
    endLine = content.find(u'\n',position)
    if endLine==-1:
      line = content[startLine+1:]
    else:
      line = content[startLine+1:endLine]
    return line, startLine+1

def findSentence(content, position):
    if len(content) == 0:
        return u''
    quotesFwd = {u'「': u'」', u'『': u'』', u"'": u"'", u'"': u'"'}
    quotesBwd = {u'」': u'「', u'』': u'『', u"'": u"'", u'"': u'"'}
    terminators = u'。．.？?！!'

    quoteStack = list()

    start = 0
    position = min(position,len(content))
    for i in xrange(position, start, -1):
        c = content[i-1]

        if not quoteStack and (c in terminators or c in quotesFwd):
            start = i
            break

        if quoteStack and c == quoteStack[0]:
            quoteStack.pop()
        elif c in quotesBwd:
            quoteStack.insert(0, quotesBwd[c])

    quoteStack = list()

    end = len(content)
    for i in xrange(position, end):
        c = content[i]

        if not quoteStack:
            if (c in terminators):
                end = i + 1
                break
            elif c == '\t':
                end = i
                break
            elif c in quotesBwd:
                end = i
                break

        if quoteStack and c == quoteStack[0]:
            quoteStack.pop()
        elif c in quotesFwd:
            quoteStack.insert(0, quotesFwd[c])   
    return content[start:end].strip(), start


def formatFields(fields, markup):
    result = dict()               
    if markup.get('line'):
      tabs = markup['line'].split('\t')
      for x in range(10):
        markup['t'+str(x)] = ''
      for i,tab in enumerate(tabs):
        markup['t'+str(i)] = tab 
    for field, value in fields.items():
        try:
            result[field] = value.format(**markup)
        except KeyError:
            pass

    return result


def splitTags(tags):
    return filter(lambda tag: tag.strip(), re.split('[;,\s]', tags))

def markupSentenceExp(definition):
    if definition.get('reading'):
        summary = u'{expression}[{reading}]'.format(**definition)
    else:
        summary = u'{expression}'.format(**definition)
    return {
        'summary': summary,
        'line': definition.get('line'),
        'filename': definition.get('filename')
    }
