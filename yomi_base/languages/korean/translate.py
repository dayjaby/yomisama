# -*- coding: utf-8 -*-

import operator
import util


class Translator:
    def __init__(self, deinflector, dictionary):
        self.deinflector = deinflector
        self.dictionary = dictionary


    def findTerm(self, text, wildcards=False):
        text = text["contentSampleFlat"]
        text = util.sanitize(text, wildcards=wildcards)

        groups = dict()

        
        length = 0
        for i in xrange(len(text), 0, -1):
            term = text[:i]
            deinflections = self.deinflector.deinflect(term, self.validator)
            groupsBefore = len(groups)
            if deinflections is None:
                self.processTerm(groups, term, wildcards=wildcards)
            else:
                for deinflection in deinflections:
                    self.processTerm(groups, **deinflection)
            if len(groups) > groupsBefore and length == 0:
                length = i

        results = map(self.formatResult, groups.items())
        results = filter(operator.truth, results)
        results = sorted(results, key=lambda d: (len(d['source'])), reverse=True)
        return results, length


    def findCharacters(self, text):
        text = util.sanitize(text, kana=False)
        results = list()

        processed = dict()
        for c in text:
            if c not in processed:
                match = self.dictionary.findCharacter(c)
                if match is not None:
                    results.append(match)
                processed[c] = match

        return results


    def processTerm(self, groups, source, rules=list(), root=str(), wildcards=False):
        root = root or source

        for entry in self.dictionary.findTerm(root, wildcards):
            key = entry['expression'], entry['hanja'], entry['glossary']
            if key not in groups:
                groups[key] = '', source, rules


    def formatResult(self, group):
        (expression, hanja, glossary), (tags, source, rules) = group
        return {
            'expression': expression,
            'hanja': hanja,
            'glossary': glossary,
            'rules': rules,
            'source': source,
            'tags': tags,
            'language': u'Korean'
        }


    def validator(self, term):
        return True
