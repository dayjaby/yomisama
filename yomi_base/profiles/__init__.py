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

import vocabulary
import kanji
import sentence
import movie

def getAllProfiles(reader):
    allProfiles = dict()
    allProfiles["kanji"] = kanji.KanjiProfile(reader)
    allProfiles["vocabulary"] = vocabulary.VocabularyProfile(reader)
    allProfiles["sentence"] = sentence.SentenceProfile(reader)
    allProfiles["movie"] = movie.MovieProfile(reader)
    return allProfiles
    
def getAllProfileClasses():
    
    allProfileClasses = dict()
    allProfileClasses["kanji"] = kanji.KanjiProfile
    allProfileClasses["vocabulary"] = vocabulary.VocabularyProfile
    allProfileClasses["sentence"] = sentence.SentenceProfile
    allProfileClasses["movie"] = movie.MovieProfile
    return allProfileClasses
    

        
