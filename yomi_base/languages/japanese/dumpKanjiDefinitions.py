#!/bin/python
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

 
import sqlite3
import json
 
def dict_factory(cursor, row):
    character = u''
    glossary = u''
    onyomi = u''
    for idx, col in enumerate(cursor.description):
        if col[0] == 'c':
            character = row[idx]
        elif col[0] == 'g':
            glossary = row[idx]
        elif col[0] == 'o':
            onyomi = row[idx]
    return (character,glossary,onyomi)
 
connection = sqlite3.connect("dictionary.db")
connection.row_factory = dict_factory
 
cursor = connection.cursor()
 
cursor.execute("select character as c, glossary as g, onyomi as o from Kanji")
 

d = dict()
for c, g, on in cursor.fetchall():
    d[c] = [g,on]
 
print json.dumps(d, separators=(',',':'))
 
connection.close()
