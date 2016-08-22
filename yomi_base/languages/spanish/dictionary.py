# -*- coding: utf-8 -*-

# Copyright (C) 2013  Alex Yatskov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
