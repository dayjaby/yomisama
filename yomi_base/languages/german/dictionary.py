# -*- coding: utf-8 -*-

import re
import os
from collections import defaultdict
import operator
import sqlite3

class Dictionary:
    def __init__(self, filename,load=True):
        dbname = filename + ".db"
        noDatabase = True
        if os.path.exists(dbname):
            if not os.path.exists(dbname):
                raise Exception("{0} does not exist".format(dbname))
            noDatabase = False
            if load:
                if os.path.exists(filename):
                    os.remove(dbname)
                    noDatabase = True
                else:
                    self.db = sqlite3.connect(dbname)
                    self.indices = set()
        if noDatabase:
            with open(filename) as file:
                if load:
                    self.db = sqlite3.connect(dbname)
                    self.indices = set()
                    cursor = self.db.cursor()
                    cursor.execute('CREATE TABLE Terms(expression TEXT, search TEXT, glossary TEXT, tags TEXT, gender TEXT)')
                    pattern = re.compile(r"^([^\#][^\{\[\t]*)(\{.*?\}|)(.*?)\t(.*?)\s([^\s]*?)$")
                    for line in file:
                        match = pattern.match(line)
                        if match:
                            match = map(lambda x: x.decode('utf-8'),match.groups())
                            search = re.sub(r"\(.*?\)",r"",match[0].strip())
                            search = re.sub(r"\s\s",r"\s",search).strip()
                            search = re.sub(r"jdm\.\s",r"",search).strip()
                            search = re.sub(r"etw\.\s",r"",search).strip()
                            search = re.sub(r"sich \s",r"",search).strip()
                            entry = (
                                (match[0]+match[2]).strip(), # expression
                                search,                    # search
                                match[3],                  # glossary
                                match[4],                  # tags
                                match[1]                  # gender
                            )
                            cursor.execute('INSERT INTO Terms VALUES(?,?,?,?,?)',entry)
                    self.db.commit()
            #os.remove(filename)


    def findTerm(self, word, wildcards=False):
        self.requireIndex('Terms', 'search')

        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM Terms WHERE search = ?', (word,))

        results = list()
        for fetch in cursor.fetchall():
            expression, search, glossary, tags, gender = fetch
            results.append({
                'expression': expression,
                'search': search,
                'glossary': glossary,
                'tags': tags.split(),
                'gender': gender
            })
        return results


    def findCharacter(self, character):
        return findTerm(self,word)


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
