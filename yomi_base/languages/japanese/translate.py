# -*- coding: utf-8 -*-

import operator
import util


class Translator:
    def __init__(self, deinflector, dictionary):
        self.deinflector = deinflector
        self.dictionary = dictionary


    def findTerm(self, text, wildcards=False):
        groups = dict()
        if wildcards and isinstance(text,list):
            self.processTerm(groups,u"".join(text),u"".join(text),root=text,wildcards=True)
        else:
            text = text["contentSampleFlat"]
            text = util.sanitize(text, wildcards=wildcards)

            for i in xrange(len(text), 0, -1):
                term = text[:i]
                deinflections = self.deinflector.deinflect(term, self.validator)
                if deinflections is None:
                    self.processTerm(groups, term, term, wildcards=wildcards)
                else:
                    for deinflection in deinflections:
                        self.processTerm(groups, term, **deinflection)

        results = map(self.formatResult, groups.items())
        results = filter(operator.truth, results)
        results = sorted(results, key=lambda d: (len(d['source']), 'P' in d['tags'],-len(d['expression']), -len(d['rules'])), reverse=True)

        length = 0
        for result in results:
            length = max(length, len(result['source']))

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


    def processTerm(self, groups, term, source, rules=list(), root=str(), wildcards=False):
        root = root or source

        for entry in self.dictionary.findTerm(root, wildcards):
            key = entry['expression'], entry['reading'], entry['glossary']
            if key not in groups:
                groups[key] = term, entry['defs'], entry['refs'], entry['tags'], source, rules


    def formatResult(self, group):
        (expression, reading, glossary), (term, defs, refs, tags, source, rules) = group
        return {
            'defs': defs,
            'refs': refs,
            'expression': expression,
            'reading': reading,
            'glossary': glossary,
            'rules': rules,
            'source': source,
            'term': term,
            'tags': tags,
            'language': u'Japanese'
        }


    def validator(self, term):
        return [d['tags'] for d in self.dictionary.findTerm(term)]
