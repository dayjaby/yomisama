# -*- coding: utf-8 -*-

import re
from collections import defaultdict

class Dictionary:
    def __init__(self, filename,load=True):
        with open(filename) as file:
            if load:
                self.entries = defaultdict(list)
                pattern = re.compile("^([^#]*?)\s(.*?)\s\[(.*?)\]\s\/(.*)\/")
                for line in file:
                    for match in pattern.findall(line):
                        modern = unicode(match[1].decode('utf-8'))
                        traditional = unicode(match[0].decode('utf-8'))
                        if modern != traditional:
                            self.entries[traditional].append({
                                'expression': traditional,
                                'reading': match[2].decode('utf-8'),
                                'glossary': match[3].decode('utf-8').replace(u"/",u"; "),
                                'language': u'Chinese',
                                'tags': u'traditional'
                            })
                        self.entries[modern].append({
                            'expression': modern,
                            'traditional': traditional,
                            'reading': match[2].decode('utf-8'),
                            'glossary': match[3].decode('utf-8').replace(u"/",u"; "),
                            'language': u'Chinese',
                        })


    def findTerm(self, word, wildcards=False):
        if wildcards:
            return [] # not yet implemented!
        elif word in self.entries:
            return self.entries[word]
        else:
            return []


    def findCharacter(self, character):
        return findTerm(self,word)
