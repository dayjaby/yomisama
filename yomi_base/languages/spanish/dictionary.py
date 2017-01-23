# -*- coding: utf-8 -*-

import re
from collections import defaultdict

class Dictionary:
    def __init__(self, filename,load=True):
        with open(filename) as file:
            if load:
                self.entries = defaultdict(list)
                pattern = re.compile(r"^([^\#][^\{\[\t]*)(\{.*?\}|)(.*?)\t(.*?)\s([^\s]*?)$")
                for line in file:
                    for match in pattern.findall(line):
                        match0 = match[0].decode('utf-8')
                        search = re.sub(r"\(.*?\)",r"",match0.strip())
                        search = re.sub(r"\s\s",r"\s",search).strip()
                        self.entries[search].append({
                            'expression': (match0+match[2].decode('utf-8')).strip(),
                            'search': search,
                            'gender': match[1].decode('utf-8'),
                            'glossary': match[3].decode('utf-8'),
                            'tags': match[4].decode('utf-8'),
                            'language': u'German',
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
