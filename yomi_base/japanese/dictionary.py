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


import operator
import sqlite3


class Dictionary:
    def __init__(self, filename, index=True):
        self.db = sqlite3.connect(filename)
        def isWord(tags):
            self.tags = tags.split(" ")
            return not set(tags.split(" ")).intersection(["p","m","f","g","h","s","u"])
        self.db.create_function("isWord",1,isWord)
        self.indices = set()


    def findTerm(self, word, wildcards=False):
        self.requireIndex('Terms', 'expression')
        self.requireIndex('Terms', 'reading')

        cursor = self.db.cursor()
        if wildcards and isinstance(word,list):
            def constr(x):
                return u"expression LIKE \"%{0}%\"".format(x)
            query = u" OR ".join(map(constr,word))
            self.query = query
            cursor.execute(u'SELECT * FROM Terms WHERE ('+query+u') AND isWord(tags) AND glossary NOT LIKE "%(obsc)%" AND glossary NOT LIKE "%(arch)%"')
        else:
            cursor.execute('SELECT * FROM Terms WHERE expression {0} ? OR reading=? LIMIT 100'.format('LIKE' if wildcards else '='), (word, word))

        results = list()
        for fetch in cursor.fetchall():
            if len(fetch)==6:
                expression, reading, glossary, tags, defs, refs = fetch
            else:
                expression, reading, glossary, tags = fetch
                defs = refs = ''
            results.append({
                'expression': expression,
                'reading': reading,
                'glossary': glossary,
                'tags': tags.split(),
                'defs': defs,
                'refs': refs
            })

        return results


    def findCharacter(self, character):
        assert len(character) == 1
        self.requireIndex('Kanji', 'character')

        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM Kanji WHERE character=? LIMIT 1', character)

        query = cursor.fetchone()
        if query is not None:
            character, kunyomi, onyomi, glossary, ongroup = query
            return {
                'character': character,
                'kunyomi': kunyomi,
                'onyomi': onyomi,
                'glossary': glossary,
                'ongroup': ongroup
            }


    def requireIndex(self, table, column):
        name = 'index_{0}_{1}'.format(table, column)
        if not self.hasIndex(name):
            self.buildIndex(name, table, column)


    def buildIndex(self, name, table, column):
        cursor = self.db.cursor()
        cursor.execute('CREATE INDEX {0} ON {1}({2})'.format(name, table, column))
        self.db.commit()


    def hasIndex(self, name):
        if name in self.indices:
            return True

        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM sqlite_master WHERE name=?', (name,))
        if len(cursor.fetchall()) == 0:
            return False

        self.indices.update([name])
        return True
