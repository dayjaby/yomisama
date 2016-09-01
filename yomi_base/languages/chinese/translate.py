# -*- coding: utf-8 -*-

# Copyright (C) 2016 David Jablonski
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

class Translator:
    def __init__(self, dictionary):
        self.dictionary = dictionary


    def findTerm(self, text, wildcards=False):
        text = text["contentSampleFlat"]
        results = []
        length = None
        for i in xrange(len(text), 0, -1):
            term = text[:i]
            for entry in self.dictionary.findTerm(term, wildcards):
                if length is None:
                    length = i
                results.append(entry)

        return results, length


    def findCharacters(self, text):
        results = []
        for i in xrange(len(text), 0, -1):
            term = text[:i]
            for entry in self.dictionary.findCharacter(root):
                results.append(entry)
        return results

    def processTerm(self, groups, source, rules=list(), root=str(), wildcards=False):
        root = root or source

        for entry in self.dictionary.findTerm(root, wildcards):
            key = entry['expression'], entry['traditional']
            if key not in groups:
                groups[key] = u'', source, rules
