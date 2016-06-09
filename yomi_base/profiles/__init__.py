import vocabulary
import kanji
import sentence

def getAllProfiles(reader):
    allProfiles = dict()
    allProfiles["kanji"] = kanji.KanjiProfile(reader)
    allProfiles["vocabulary"] = vocabulary.VocabularyProfile(reader)
    allProfiles["sentence"] = sentence.SentenceProfile(reader)
    return allProfiles
    
def getAllProfileClasses():
    
    allProfileClasses = dict()
    allProfileClasses["kanji"] = kanji.KanjiProfile
    allProfileClasses["vocabulary"] = vocabulary.VocabularyProfile
    allProfileClasses["sentence"] = sentence.SentenceProfile
    return allProfileClasses
    

        