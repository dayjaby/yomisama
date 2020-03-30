# -*- coding: utf-8 -*-

import codecs
import json
import re

from .jcconv import *

#
# Deinflection
#

class Deinflection:
    def __init__(self, term, tags=list(), rule=str()):
        self.children = list()
        self.term = term
        self.tags = tags
        self.rule = rule
        self.success = False


    def validate(self, validator):
        for tags in validator(self.term):
            if len(self.tags) == 0:
                return True

            for tag in self.tags:
                if self.searchTags(tag, tags):
                    return True

    def deinflect(self, validator, rules):
        if self.validate(validator):
            child = Deinflection(self.term)
            self.children.append(child)

        for rule, variants in rules.items():
            for variant in variants:
                tagsIn = variant['tagsIn']
                tagsOut = variant['tagsOut']
                kanaIn = variant['kanaIn']
                kanaOut = variant['kanaOut']

                allowed = len(self.tags) == 0
                for tag in self.tags:
                    if self.searchTags(tag, tagsIn):
                        allowed = True
                        break

                if not allowed or not self.term.endswith(kanaIn):
                    continue

                term = self.term[:-len(kanaIn)] + kanaOut

                child = Deinflection(term, tagsOut, rule)
                if child.deinflect(validator, rules):
                    self.children.append(child)

        if len(self.children) > 0:
            return True


    def searchTags(self, tag, tags):
        for t in tags:
            if re.search(tag, t):
                return True


    def gather(self):
        if len(self.children) == 0:
            return [{'root': self.term, 'rules': list()}]

        paths = list()
        for child in self.children:
            for path in child.gather():
                if self.rule:
                    path['rules'].append(self.rule)
                path['source'] = self.term
                paths.append(path)

        return paths


#
# Deinflector
#

class Deinflector:
    def __init__(self, filename):
        with codecs.open(filename, 'rb', 'utf-8') as fp:
            self.rules = json.load(fp)


    def deinflect(self, term, validator):
        node = Deinflection(term)
        if node.deinflect(validator, self.rules):
            return node.gather()
        else:
            node = Deinflection(kata2hira(term))
            if node.deinflect(validator, self.rules):
                return node.gather()
