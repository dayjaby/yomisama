import reader_util
import time
import os
import re


class FileState:
    def __init__(self,fn,stripReadings,languages=[],profiles={}):
        self.alias = dict()
        self.languages = languages
        self.profiles = dict()
        self.loadedExtensions = []
        for k, profile in profiles.items():
            self.profiles[profile.name] = {
                'wordsAll': dict(),
                'wordsBad': dict(),
                'wordsMarkup': dict(),
                'wordsNotFound': [],
                'descriptor': profile.descriptor,
                'allowedTags': profile.allowedTags,
                'freshlyAdded': [],
                'longestMatch': None,
                'longestMatchKey': ''
            }
        self.sep = u"\U00012000"
        self.lineBreak = u"\U00012001"
        self.dueness = 0.0
        self.wrong = 0
        self.correct = 0
        self.resetTimer()
        self.stripReadings = stripReadings
        if fn is None:
            self.filename = u''
            self.basename = u''
            self.name = u''
        else:
            self.filename = unicode(fn)
            self.name = os.path.splitext(self.filename)[0]
            self.basename = os.path.basename(self.name)
            self.load()
    
    def count(self,name):
        cnt = 0
        for k,profile in self.profiles.items():
            cnt += len(profile[name])
        return cnt
    
    def load(self):
        with open(self.filename) as fp:
            self.content = fp.read()

        self.content, self.encoding = reader_util.decodeContent(self.content)
        if self.stripReadings:
            self.content = reader_util.stripReadings(self.content)
    

    def resetTimer(self):
        self.timerStarted = time.time()

    def getExportVocabularyList(self,profile):
        profile = self.profiles[profile]
        def access(x,y):
            if y not in x or x[y] is None:
                return u''
            else:
                return x[y]
        #don't export filename, because it's unnecessary for importing
        allowedTags = profile["allowedTags"][:]
        if 'filename' in allowedTags:
            allowedTags.remove('filename')
        vocabularyDefinitions = [self.sep.join([x.replace(u'\n',self.lineBreak).replace(u"\r","")]+([access(profile['wordsMarkup'][x],y).replace(u'\n',self.lineBreak).replace(u"\r","") for y in allowedTags])) for x in profile['wordsAll'].keys()]
        return u'### ' + profile["descriptor"] + ' ###\n'+ self.sep.join(allowedTags) +(u'\n' if len(vocabularyDefinitions)>0 else '')+ u'\n'.join(vocabularyDefinitions)+u'\n'.join(profile['wordsNotFound']) 
    
    def getAliasList(self):
        if not self.alias.items():
            return u''
        else:
            return u'### ALIAS ###\n' + u'\n'.join([eng + self.sep + jpn for eng,jpn in self.alias.items()]) + u'\n'
    
    def overwriteVocabulary(self,profile,value,card):
        profile = self.profiles[profile]
        profile['wordsAll'][value] = card
        if value in profile['wordsBad']:
            profile['wordsBad'][value] = card
    
    
    def addVocabulary(self,profile,value,card,addToBadListToo = True):
        profile = self.profiles[profile]
        profile['wordsAll'][value] = card
        if addToBadListToo:
            profile['wordsBad'][value] = card             
    
    def addMarkup(self,profile,value,markup):
        profile = self.profiles[profile]
        profile['wordsMarkup'][value] = markup
        
    def findVocabulary(self,sched,allCards,needContent=True):
        lines = self.content.splitlines()
        state = "text"
        currentProfile = None
        self.exportedVocab = False
        exportedTags = None
        self.content = u''
        self.dueness = 0.0
        self.foundvocabs = 0
        shuffle = False
        regexText = False
        filteredLines = []
        for line in lines:
            if self.exportedVocab and not exportedTags and state == "profile":
                exportedTags = line.split(self.sep)
            elif line == u'### REGEXP ###':
                state = "regex"
                regexText = True
                currentProfile = "vocabulary"
            elif line == u'### SHUFFLE THIS TEXT ###':
                shuffle = True
            elif line == u'### ALIAS ###':
                state = "alias"
            elif line == u'### MECAB ###':
                state = "mecab"
            elif line == u'### VOCABULARY IN THIS TEXT ###':
                state = "profile"
                currentProfile = "vocabulary"
            elif line == u'### SENTENCES IN THIS TEXT ###':
                state = "profile"
                currentProfile = "sentence"
                self.exportedVocab = True
                exportedTags = False
            elif line == u'### KANJI IN THIS TEXT ###':
                state = "profile"
                currentProfile = "kanji"
                self.exportedVocab = True
                exportedTags = False
            elif line == u'### MOVIE SNIPPETS ###':
                state = "profile"
                currentProfile = "movie"
                self.exportedVocab = True
                exportedTags = False
            elif line == u'### VOCABULARY IN THIS TEXT (EXPORT)###' or line == u'### VOCABULARY IN THIS TEXT (EXPORT) ###':
                state = "profile"
                currentProfile = "vocabulary"
                self.exportedVocab = True
                exportedTags = False
            elif state == "regex":
                infos = line.split("###")
                if len(infos) == 3:
                    regex, field, alias = infos
                    regex = re.compile(regex)
                    for k,profile in allCards.items():
                        for key,card in profile.items():
                            note = card.note()
                            if regex.match(key):
                                if k == currentProfile:
                                    if alias in note.keys():
                                        self.alias[note[alias]] = note[field]
                                        filteredLines.append(note[alias])
                                    else:
                                        filteredLines.append(note[field])
                                    import aqt
                                    aqt.mw.col.profiles = self.profiles
                                    self.profiles[k]['wordsMarkup'][key] = note.fields
                                    self.dueness += sched._smoothedIvl(card)
                                    self.profiles[k]['wordsAll'][key] = card
                                    self.foundvocabs += 1
            elif state == "mecab":
                self.exportedVocab = True
                definitions = line.split(self.sep)
                line = definitions.pop(0)
                markup = dict()
                markup['summary'] = line
                markup['expression'] = definitions[0]
                markup['reading'] = definitions[1]
                markup['kanji'] = u""
                markup['hanja'] = u""
                if "japanese" in self.languages:
                    definition = self.languages["japanese"].dictionary.findTerm(word=definitions[0],reading=definitions[1])
                    if len(definition)>0:
                        markup['glossary'] = definition[0]['glossary']
                    else:
                        markup['glossary'] = u""
                markup['line'] = definitions[2]
                markup['sentence'] = definitions[3]
                markup['traditional'] = u""
                markup['language'] = u"Japanese"
                markup['filename'] = self.filename
                self['wordsMarkup'][line] = markup
                if line in allCards:
                    card = allCards[line]
                    self.dueness += sched._smoothedIvl(card)
                    self['wordsAll'][line] = card
                    self.foundvocabs += 1
                else:
                    self['wordsNotFound'].append(line)
            elif state == "profile":
                if self.exportedVocab:
                    definitions = line.split(self.sep)
                    line = definitions.pop(0)
                    markup = dict()
                    for i, field in enumerate(definitions):
                        if i>= len(exportedTags):
                            break
                        markup[exportedTags[i]] = field.replace(self.lineBreak,u'\n')
                    markup['filename'] = self.filename
                    self.profiles[currentProfile]['wordsMarkup'][line] = markup
                if line in allCards[currentProfile]:
                    card = allCards[currentProfile][line]
                    self.dueness += sched._smoothedIvl(card)
                    self.profiles[currentProfile]['wordsAll'][line] = card
                    self.foundvocabs += 1
                else:
                    self.profiles[currentProfile]['wordsNotFound'].append(line)
            elif state == "alias":
                eng,jpn = line.split(self.sep)
                self.alias[eng] = jpn
            elif needContent:
                filteredLines.append(line)
        if shuffle:
            import random
            random.shuffle(filteredLines)
            if not regexText:
                filteredLines.append(u'### SHUFFLE THIS TEXT ###')
        self.content = u'\n'.join(filteredLines) + u'\n'
        
    def onLearnVocabularyList(self,sched):
        self.correct = 0
        self.wrong = 0
        self.timeTotal = time.time() - self.timerStarted
        countWords = 0
        for k,profile in self.profiles.items():
            countWords += len(profile['wordsAll'])
        self.timePerWord = self.timeTotal / countWords if countWords > 0 else 0
        for k,profile in self.profiles.items():
            for word in profile['wordsAll']:
                if word in profile['wordsBad']:
                    sched.earlyAnswerCard(profile['wordsBad'][word],1,self.timePerWord)
                    self.wrong += 1
                else:
                    sched.earlyAnswerCard(profile['wordsAll'][word],3,self.timePerWord)
                    self.correct += 1
