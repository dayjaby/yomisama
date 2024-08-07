# -*- coding: utf-8 -*-

from . import vocabulary
from . import kanji
from . import sentence
# from . import movie

def getAllProfiles(reader):
    allProfiles = dict()
    allProfiles["kanji"] = kanji.KanjiProfile(reader)
    allProfiles["vocabulary"] = vocabulary.VocabularyProfile(reader)
    allProfiles["sentence"] = sentence.SentenceProfile(reader)
    # allProfiles["movie"] = movie.MovieProfile(reader)
    return allProfiles

def getAllProfileClasses():
    allProfileClasses = dict()
    allProfileClasses["kanji"] = kanji.KanjiProfile
    allProfileClasses["vocabulary"] = vocabulary.VocabularyProfile
    allProfileClasses["sentence"] = sentence.SentenceProfile
    # allProfileClasses["movie"] = movie.MovieProfile
    return allProfileClasses
