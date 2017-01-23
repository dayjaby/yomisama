# -*- coding: utf-8 -*-

import operator
import sqlite3


class Dictionary:
    def __init__(self, filename, index=True, load=True):
        with open(filename) as file:
            pass
        if load:
            self.db = sqlite3.connect(filename)
            self.indices = set()


    def findTerm(self, word, wildcards=False):
        self.requireIndex('Terms', 'expression')

        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM Terms WHERE expression {0} ? LIMIT 100'.format('LIKE' if wildcards else '='),(word,))

        results = list()
        for expression, glossary, hanja in cursor.fetchall():
            results.append({
                'expression': expression,
                'hanja': hanja,
                'glossary': glossary
            })

        return results


    def findCharacter(self, character):
        # not implemented
        return None
        
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
